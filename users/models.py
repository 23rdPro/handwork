from __future__ import absolute_import, unicode_literals
import os

from django.contrib import auth
from django.core.exceptions import ValidationError
from django.contrib.auth.models import PermissionsMixin, Group
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models, transaction
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from six import python_2_unicode_compatible
from phonenumber_field.modelfields import PhoneNumberField

from .image_compress import compress

from future import standard_library

standard_library.install_aliases()


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        if not email and not username:
            raise ValueError(_('Email and Username are required'))
        if extra_fields.get('is_active') is not True:
            raise ValueError('User must be active')
        email = self.normalize_email(email)
        user_model = User
        username = user_model.normalize_username(username)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not False:
            raise ValueError('This action is not permitted')
        if extra_fields.get('is_staff') is not False:
            raise ValueError('This action is not permitted')
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('superuser must be is_staff=True.'))
        return self._create_user(email, username, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


@python_2_unicode_compatible
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, help_text='user email address', max_length=255)
    username = models.CharField(_('username'), unique=True, max_length=37, help_text='account unique moniker')
    # First Name and Last Name do not cover name patterns around the globe.
    name = models.CharField(_('Full name'), max_length=128, help_text='full name')
    mobile = PhoneNumberField(_('Mobile number'), help_text='mobile number')
    avatar = models.ImageField(_('Avatar'), upload_to='avatars', help_text='Max: 5MB', max_length=255)
    __avatar = None
    is_worker = models.BooleanField(_('Worker'), default=False, help_text='register as a worker')
    is_client = models.BooleanField(_('Client'), default=False, help_text='register as a client')
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    is_active = models.BooleanField(_('active status'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]  # useful for `createsuperuser` command

    objects = UserManager()

    class Meta:
        ordering = ['created_at']

    # __init__ provides a way to decide if compress(image) should be called by assigning self.avatar to
    # self.__avatar and checking for equality at each save()
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__avatar = self.avatar

    def clean(self):
        if self.is_worker and self.is_client:
            raise ValidationError(_('You can not register for both Worker and Client simultaneously'))

        if self.name and len(str(self.name).split()) < 2:  # may not be generally applicable, but works for now TODO
            raise ValidationError(_('Please provide your full name'))

        if self.username and len(str(self.username).split()) > 1:
            raise ValidationError(_("Please provide username without space"))

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.avatar:
            if self.avatar.name != self.__avatar.name:
                new_image = compress(self.avatar)
                old_img = self.__avatar
                print(old_img)
                self.avatar = new_image
                try:
                    os.remove('media/%s' % old_img.name)
                except PermissionError or FileNotFoundError:
                    pass

        instance = super(User, self).save(force_insert, force_update, *args, **kwargs)
        transaction.on_commit(self.update_user_group)
        self.__avatar = self.avatar
        return instance

    def update_user_group(self):
        if self.is_worker:
            self.groups.set([g.pk for g in Group.objects.filter(name='workers')])
        elif self.is_client:
            self.groups.set([g.pk for g in Group.objects.filter(name='clients')])

    def __str__(self):
        return self.get_username()

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

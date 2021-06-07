from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
# from phonenumber_field.formfields import PhoneNumberField

from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True, help_text='unique email address')

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'username')


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(max_length=255, required=True, help_text='unique email address')

    class Meta(UserChangeForm):
        model = User
        fields = ('email', 'username')

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5*1024*1024:
                raise ValidationError(_('Image too large. Max size (5MB)'))
            return avatar
        else:
            raise ValidationError(_('Couldn\'t read uploaded image. Upload another file'))


class UpdateUserAfterSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'mobile', 'avatar', 'is_client', 'is_worker']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 5*1024*1024:
                raise ValidationError(_('Image too large. Max size (5MB)'))
            elif len(avatar.name) > 255:
                raise ValidationError(_('avatar name is too long'))
            return avatar
        else:
            raise ValidationError(_('Couldn\'t read uploaded file. Upload another image'))

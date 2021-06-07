from __future__ import absolute_import, unicode_literals

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from six import python_2_unicode_compatible
from future import standard_library

from .managers import WorkerManager
from users.models import User

standard_library.install_aliases()


@python_2_unicode_compatible
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client',
                                help_text='name of client')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        pass

    def __str__(self):
        return self.user.get_username()

    def get_absolute_url(self):
        return reverse('profession:client_detail', kwargs={'username': self.user.get_username()})


INDUSTRY_CHOICES = (
    (1, _('Aviation')),
    (2, _('Arts')),
    (3, _('Business')),
    (4, _('Education')),
    (5, _('Law Enforcement')),
    (6, _('Media')),
    (7, _('Medical')),
    (8, _('Service Industry')),
    (9, _('Technology')),
    (10, _('Others'))
)


@python_2_unicode_compatible
class Worker(models.Model):  # TODO: payment integration
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker',
                                help_text='name of worker')
    is_approved = models.BooleanField(_('certified'), default=False, help_text='available for engagements')
    is_engaged = models.BooleanField(_('engaged'), default=False, help_text='available for engagements')
    query = models.SmallIntegerField(_('unprofessional conduct'), default=0, help_text='number of queries')
    ratings = models.SmallIntegerField(_('ratings'), default=0, help_text='worker\'s rating')

    industry = models.PositiveSmallIntegerField(_('Industry'), choices=INDUSTRY_CHOICES, null=True,
                                                help_text='select industry category')
    profession = models.CharField(_('profession'), max_length=128, null=True,
                                  help_text='area of expertise, e.g Full Stack Developer')
    qualifications = models.TextField(_('qualifications'), max_length=255, null=True,
                                      help_text='formal/informal education')
    sales_pitch = models.TextField(_('business description'), max_length=255, help_text='sell your business', null=True)
    address = models.CharField(_('business address'), max_length=128, help_text='head office', null=True)
    registration = models.CharField(_('business registration number'), max_length=128, null=True,
                                    help_text='CAC for instance')
    estimate = models.DecimalField(_('estimate/unit'), help_text='charges in Naira per unit of work eg (25000.00)',
                                   decimal_places=2, max_digits=10, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = WorkerManager()

    class Meta:
        ordering = ['-timestamp', '-updated']

    def __str__(self):
        return self.user.get_username()

    def get_absolute_url(self):
        return reverse('workers:worker_detail', kwargs={'username': self.user.get_username()})

    def get_update_url(self):
        return "%sedit-profile" % self.get_absolute_url()

    def get_delete_url(self):
        return "%sdelete-profile" % self.get_absolute_url()

    def get_query_val(self):
        return self.query

    def certify_worker(self):
        if self.get_query_val() > 2:
            self.is_approved = False
        else:
            self.is_approved = True


@python_2_unicode_compatible
class Engage(models.Model):
    # request (client)
    # a client requests for a specific service (profession), unit is a way of knowing in what quantity
    # when a worker is notified and they accept, that particular request becomes locked and no
    # longer available for reroute (to another worker). When engagement is concluded, the worker
    # becomes available for a new gig
    # TODO profession will be a search field, it must support partial match when filtering workers by profession

    client = models.ForeignKey(User, on_delete=models.CASCADE, help_text='client identification',
                               related_name='engaging_client')
    profession = models.CharField(_('Hire a/an'), max_length=128,
                                  help_text='name of profession you \'d like to engage e.g Full Stack Developer')
    unit = models.SmallIntegerField(_('units'), default=1, help_text='for instance, 1 complete suit outfit')
    estimate = models.DecimalField(_('estimate/unit'), help_text='charges per unit of work', decimal_places=2,
                                   max_digits=6, null=True, blank=True)

    # response (worker)
    worker = models.ForeignKey(User, on_delete=models.CASCADE, help_text='worker identification',
                               related_name='engaging_worker')

    # admin / client / worker
    is_locked = models.BooleanField(_('locked'), default=False, help_text='available for reroute?')
    concluded = models.BooleanField(_('concluded'), default=False, help_text='gig concluded')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name = 'engagement'
        verbose_name_plural = 'engagements'
        ordering = ('-created_at', '-updated_at')

    def __str__(self):
        return self.profession

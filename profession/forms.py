from django import forms
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

from profession.models import Engage, Worker
from users.models import User


class EngagementForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(EngagementForm, self).__init__(user, *args, **kwargs)
        self.fields['client'].queryset = User.objects.filter(username=user)

    client = forms.CharField(required=True, max_length=37, initial='issokay')

    class Meta:
        model = Engage
        fields = ['client', 'profession', 'unit', 'worker', 'is_locked', 'concluded']


class WorkerForm(forms.ModelForm):

    class Meta:
        model = Worker
        fields = ['industry', 'profession', 'qualifications', 'sales_pitch', 'address', 'registration', 'estimate']

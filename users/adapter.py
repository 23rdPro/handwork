from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.shortcuts import resolve_url
from django.urls import reverse


class UserAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        if request.user.is_authenticated and (not request.user.name and not request.user.avatar and
                                              not request.user.mobile):
            return reverse('users:complete_signup', kwargs={'username': request.user.username})

        else:
            return resolve_url(settings.LOGIN_REDIRECT_URL)

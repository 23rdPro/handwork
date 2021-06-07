from __future__ import absolute_import, unicode_literals

from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('<str:username>/', views.UserDetailView.as_view(), name='detail'),
    path('<str:username>/complete-signup/', views.UpdateUserAfterSignupView.as_view(), name='complete_signup'),
]


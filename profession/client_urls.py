from __future__ import absolute_import, unicode_literals

from django.contrib.auth.decorators import permission_required
from django.urls import path
from . import views


urlpatterns = [
    path('<str:username>/', views.ClientDetailView.as_view(), name='client_detail'),

]

from __future__ import absolute_import, unicode_literals

from django.contrib.auth.decorators import permission_required
from django.urls import path
from . import views


urlpatterns = [
    path('<str:username>/', views.WorkerDetailView.as_view(), name='worker_detail'),
    path('<str:username>/edit-profile/', views.WorkerUpdateView.as_view(), name='worker_update'),

]

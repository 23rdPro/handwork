from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import UpdateView, DetailView, DeleteView, ListView, TemplateView
from django.contrib import messages

from profession.models import Client, Worker
from .models import User
from .forms import UpdateUserAfterSignupForm

# orm, permission, groups, caches


class UpdateUserAfterSignupView(LoginRequiredMixin, UpdateView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    form_class = UpdateUserAfterSignupForm
    template_name = 'users/user_update.html'
    context_object_name = 'user'

    def get_success_url(self):
        if self.request.user.is_client:
            return reverse_lazy('clients:client_detail', kwargs={'username': self.object.username})
        elif self.request.user.is_worker:
            return reverse_lazy('workers:worker_detail', kwargs={'username': self.object.username})


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'users/user_detail.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, username=self.request.user.username)



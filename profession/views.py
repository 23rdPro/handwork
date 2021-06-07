from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import UpdateView, DetailView, DeleteView, CreateView, FormView
from django.contrib import messages

from users.models import User
from .models import Worker, Engage, Client
from .forms import EngagementForm, WorkerForm


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    template_name = 'client/client_detail.html'
    context_object_name = 'client'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, user__username=self.request.user.username)


# class ClientUpdateView(LoginRequiredMixin, UpdateView):
#     model = Client
#     fields = ['name', ]
#     context_object_name = 'client'
#     template_name = 'client/client_update.html'


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    form_class = WorkerForm
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    context_object_name = 'worker'
    template_name = 'worker/worker_update.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('worker.can_change_worker'):
            return HttpResponseForbidden()
        return super(WorkerUpdateView, self).dispatch(request, *args, **kwargs)


class WorkerDetailView(LoginRequiredMixin, DetailView):
    model = Worker
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    template_name = 'worker/worker_detail.html'
    context_object_name = 'worker'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, user__username=self.request.user.username)


# class ProfessionCreateView(LoginRequiredMixin, CreateView):
#     model = Profession
#     template_name = 'profession/profession_form.html'
#     fields = ['industry', 'name', 'qualifications', 'sales_pitch', 'address', 'registration', 'estimate']


# class ProfessionFormView(LoginRequiredMixin, FormView):
#     template_name = 'profession/profession_form.html'
#     form_class = ProfessionForm
#     success_url = 'users:detail'
#
#     def form_valid(self, form):
#         return super(ProfessionFormView, self).form_valid(form)


# class EngagementCreateView(LoginRequiredMixin, CreateView):
#     model = Engage
#     template_name = 'engage/create_engagement.html'
#     form_class = EngagementForm
#
#
# class EngagementFormView(LoginRequiredMixin, FormView):
#     pass
#
#
# class EngagementDetailView(LoginRequiredMixin, DetailView):
#     model = Engage
#     template_name = 'engage/engagement_detail.html'
#
#
# class EngagementUpdateView(LoginRequiredMixin, UpdateView):
#     model = Engage

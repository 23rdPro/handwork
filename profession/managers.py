from __future__ import absolute_import, unicode_literals

from django.db import models
from django.db.models import Q
from future import standard_library

standard_library.install_aliases()


class WorkerQuerySet(models.QuerySet):
    def engaged(self):
        # return self.exclude(Q(is_approved=False) & Q(is_engaged=False) & Q(query__gte=2))
        return self.filter(Q(is_approved=True) & Q(is_engaged=True) & Q(query__lte=2))

    def not_engaged(self):
        return self.filter(Q(is_approved=True) & Q(is_engaged=False) & Q(query__lte=2))

    def filter_by_profession(self, query):
        lookup = (
                Q(industry__icontains=query) |
                Q(profession__icontains=query) |
                Q(qualifications__icontains=query) |
                Q(sales_pitch__icontains=query) |
                Q(address__icontains=query)
        )
        return self.filter(lookup)

    def search(self, query):
        lookup = (
                Q(name__username__icontains=query) |
                Q(name__name__icontains=query) |
                Q(name__mobile__icontains=query) |
                Q(industry__icontains=query) |
                Q(profession__icontains=query) |
                Q(qualifications__icontains=query) |
                Q(sales_pitch__icontains=query) |
                Q(address__icontains=query)
        )
        return self.filter(lookup)


class WorkerManager(models.Manager):
    def get_queryset(self):
        return WorkerQuerySet(self.model, using=self._db)

    def engaged(self):
        return self.get_queryset().engaged()

    def not_engaged(self):
        return self.get_queryset().not_engaged()

    def filter_by_profession(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().not_engaged().filter_by_profession(query)

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().not_engaged().search(query)

from django.db.models import Prefetch, Count
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from users.models import User


# @receiver(m2m_changed, sender=User.groups.through)
# def update_user_group(sender, action, pk_set, instance=None, **kwargs):
#     if action in ['post_add', 'post_remove']:
#         if instance.is_client:
#             instance.groups.add([g.pk for g in Group.objects.filter(name='clients')][0])
#         elif instance.is_worker:
#             instance.groups.add([g.pk for g in Group.objects.filter(name='workers')][0])

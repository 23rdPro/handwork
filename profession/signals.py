from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from profession.models import Worker, Client


@receiver(post_save, sender=User)
def create_user_status(sender, instance, **kwargs):
    if instance.is_client:
        client, created = Client.objects.get_or_create(user=instance)
        try:
            if created and Worker.objects.get(user=instance):
                Worker.objects.filter(user=instance).delete()
        except Exception as e:
            print(e)
        if created:
            client.save()

    elif instance.is_worker:
        worker, created = Worker.objects.get_or_create(user=instance)
        try:
            if created and Client.objects.get(user=instance):
                Client.objects.filter(user=instance).delete()
        except Exception as e:
            print(e)
        if created:
            worker.save()

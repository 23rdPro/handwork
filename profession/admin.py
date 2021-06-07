from django.contrib import admin

from .models import Client, Worker, Engage

admin.site.register(Client)
admin.site.register(Worker)
admin.site.register(Engage)

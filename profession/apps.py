from django.apps import AppConfig


class ProfessionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profession'

    def ready(self):
        import profession.signals

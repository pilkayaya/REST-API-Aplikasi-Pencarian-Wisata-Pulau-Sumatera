from django.apps import AppConfig


class WisataAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wisata_app'

    def ready(self):
        from . import signals

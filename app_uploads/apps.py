from django.apps import AppConfig


class AppUploadsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_uploads'

    def ready(self):
        import app_uploads.signals
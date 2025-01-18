from django.apps import AppConfig


class StatpoolsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'statpools'

    def ready(self):
        return super().ready()

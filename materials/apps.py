from django.apps import AppConfig


class MaterialsConfig(AppConfig):
    name = 'materials'
    verbose_name = 'Навчання та продажі'

    def ready(self):
        from . import signals  # noqa: F401

from django.apps import AppConfig


class ContentRelationsAppConfig(AppConfig):
    name = 'contentrelations'
    verbose_name = 'Content Relations'

    def ready(self):
        from contentrelations import autodiscover
        autodiscover()

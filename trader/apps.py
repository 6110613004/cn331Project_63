from django.apps import AppConfig


class TraderConfig(AppConfig):
    name = 'trader'

    def ready(self):
        import trader.signals

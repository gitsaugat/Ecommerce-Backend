from django.apps import AppConfig


class SupportConfig(AppConfig):
    name = 'support'

    def ready(self) -> None:
        import support.signals

from django.apps import AppConfig
from django.utils import timezone


class AirflowsConfig(AppConfig):
    name = 'airflows'

    def ready(self) -> None:
        from .services import set_currency
        set_currency(timezone.now().date())
        return super().ready()

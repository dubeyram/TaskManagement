from django.apps import AppConfig
import logging.config
from django.conf import settings

class UsersTasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_tasks"

    def ready(self):
        """
        Import signals
        """
        import user_tasks.signals

class MyAppConfig(AppConfig):
    name = "user_tasks"

    def ready(self):
        logging.config.dictConfig(settings.LOGGING)
        logging.getLogger(__name__).info("Logging configured successfully.")
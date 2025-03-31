from django.apps import AppConfig


class UsersTasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_tasks"

    def ready(self):
        """
        Import signals
        """
        import user_tasks.signals

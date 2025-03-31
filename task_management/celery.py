import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_management.settings")
celery_app = Celery("task_management")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()

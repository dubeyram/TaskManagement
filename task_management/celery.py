"""
Celery configuration for the Task Management application.

This module initializes the Celery app and loads the Celery configuration from Django settings.
It also auto-discovers and registers Celery tasks.
"""
import os
from celery import Celery


# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_management.settings")

# Initialize Celery app
celery_app = Celery("task_management")

# Load Celery configuration from Django settings
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover and register Celery tasks
celery_app.autodiscover_tasks()

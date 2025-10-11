"""
Signals for User Tasks
"""

from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from user_tasks.models import User
from django.core.mail import send_mail
from .tasks import send_welcome_email
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def new_user_created(sender, instance, created, **kwargs):
    """
    Signal when a new user is created
    """

    if created:
        send_welcome_email.delay(instance.email, instance.username)
        logger.info(f"User Created for email: {instance.email}")


user_task_assigned = Signal()


@receiver(user_task_assigned)
def user_task_assigned_(signal, task, extra_data, **kwargs):
    """
    Signal when a user is assigned to a task
    """
    logger.info(
        f"Task: {task.get('name')} is assigned to a these users: {extra_data.get('user_id')}"
    )


create_task = Signal()


@receiver(create_task)
def task_created(signal, task, extra_data, **kwargs):
    """
    Signal when a new task is created
    """
    if extra_data.get("created"):
        if not task.get("assigned_users"):
            logger.info(
                f"New task: {task.get('name')} created successfully, but not assigned to any users yet."
            )
        else:
            logger.info(
                f"New task: {task.get('name')} created successfully, and assigned to these users: {task.get('assigned_users')}"
            )
    else:
        logger.error(f"Unable to create task: {kwargs.get('error')}")

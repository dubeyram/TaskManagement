"""
Celery tasks for the Task Management application.

This module provides Celery tasks for:
- Sending welcome emails to new users
- Sending daily reminder emails to users
"""

from celery import shared_task
from django.core.mail import send_mail
from user_tasks.models import User
from task_management.config import EMAIL_FROM
import logging

logger = logging.getLogger(__name__)



@shared_task
def send_welcome_email(email, username):
    """Send a welcome email to a new user."""
    subject = "Welcome to Our Platform!"
    message = f"Hello {username},\n\nThank you for joining us!"
    from_email = EMAIL_FROM
    
    send_mail(subject, message, from_email, [email])
    logger.info("Mail Sent Successfully using celery")
    return f"Email sent to {email}"


@shared_task
def send_daily_reminder():
    """Send a daily reminder email to users."""
    all_users_email = User.objects.all().values_list('email', flat=True)
    
    subject = "Daily Reminder"
    message = "This is your scheduled daily reminder."
    sender = "rambackenddev@gmail.com"
    recipients = all_users_email
    send_mail(subject, message, sender, recipients)
    return "Daily reminder email sent!"
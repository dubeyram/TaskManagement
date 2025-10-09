"""
Models for the Task Management application.

This module defines:
- `User`: Custom user model extending Django's `AbstractUser`
- `Task`: Task model representing a task in the system
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from user_tasks.manager import UserManager

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Fields:
        - `username` (CharField): Unique username for the user.
        - `email` (EmailField): Unique email address for the user.
        - `mobile` (CharField): Optional mobile number for the user.
    Methods:
        - `__str__`: Returns the user's first name or username.
        - `save`: Overrides save method to normalize username and email.
    """
    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    mobile = models.CharField(max_length=15, unique=True, blank=True, null=True)

    objects = UserManager() # type: ignore

    def __str__(self):
        return self.first_name or self.username

    def save(self, *args, **kwargs):
        if self.username:
            self.username = self.username.lower().strip()
        if self.email:
            self.email = self.email.lower().strip()
        super().save(*args, **kwargs)


class Task(models.Model):
    """
    Model representing a task in the system.

    Fields:
        - `name` (CharField): Name of the task.
        - `description` (TextField): Detailed description of the task.
        - `created_at` (DateTimeField): Timestamp when the task was created.
        - `completed_at` (DateTimeField, optional): Timestamp when the task was completed.
        - `task_type` (CharField): Type/category of the task.
        - `status` (CharField): Current status of the task (Pending, In Progress, Completed).
        - `assigned_users` (ManyToManyField): Users assigned to this task.

    Methods:
        - `__str__`: Returns the name of the task.
    """

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    task_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    assigned_users = models.ManyToManyField(User, related_name="tasks")

    def __str__(self):
        return self.name

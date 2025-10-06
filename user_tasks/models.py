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
from django.contrib.auth.hashers import make_password
from task_management.utils import generate_secure_password


class UserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        username = username or email

        if not password:
            password = generate_secure_password()

        user = self.model(
            username=username.lower().strip(),
            email=email.lower().strip(),
            **extra_fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
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

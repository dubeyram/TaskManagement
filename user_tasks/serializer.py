"""
Serializers for task management application.

This module provides serializers for handling:
- Task creation and updates
- Assigning users to tasks
- User creation and authentication
- Retrieving tasks assigned to users
"""

from rest_framework import serializers
from .models import Task, User


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    Handles task creation and updates while enforcing required fields.
    """

    class Meta:
        model = Task
        fields = "__all__"
        extra_kwargs = {
            "name": {"required": True},
            "description": {"required": True},
            "task_type": {"required": False},
            "status": {"required": False},
            "assigned_users": {"required": False},
        }


class TaskAssignSerializer(serializers.ModelSerializer):
    """
    Serializer for assigning users to a task.

    Uses PrimaryKeyRelatedField to associate users efficiently.
    """

    assigned_users = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.only("id"), many=True
    )

    class Meta:
        model = Task
        fields = ["assigned_users", 'name']
        extra_kwargs={
            "name": {"required": False}
        }


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    - Ensures `password` is write-only for security.
    - `username` is read-only since it will be auto-generated.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password", "mobile"]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": False},
            "email": {"required": True},
            "username": {"read_only": True},
            "password": {"write_only": True},
        }


class UserTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving tasks assigned to a user.

    Returns minimal task details to reduce payload size.
    """

    class Meta:
        model = Task
        fields = ["name", "description", "task_type", "status"]

"""
Gateway functions for the Task Management application.

This module provides helper functions for:
- Creating users and tasks
- Listing and retrieving tasks
- Assigning tasks to users
- Fetching tasks assigned to a specific user
"""

from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from .models import Task, User
from .serializer import TaskSerializer, TaskAssignSerializer, UserTaskSerializer
from task_management import config


def create_user(serializer):
    """
    Create a new user and return the serialized object.

    - Hashes the password before saving.
    - Generates a unique username based on email prefix + epoch timestamp.

    Args:
        serializer (UserSerializer): Validated serializer containing user data.

    Returns:
        User: The newly created user instance.
    """
    serializer.validated_data["password"] = make_password(
        serializer.validated_data["password"]
    )
    username = serializer.validated_data["email"].split("@")[0]
    epoch_time = int(now().timestamp())
    serializer.validated_data["username"] = f"{username}_{epoch_time}"

    return serializer.save()


def create_task(serializer):
    """
    Create a new task and return the serialized object.

    Args:
        serializer (TaskSerializer): Validated serializer containing task data.

    Returns:
        Task: The newly created task instance.
    """
    return serializer.save()


def list_tasks(page, page_size, order_by):
    """
    Retrieve a paginated list of tasks sorted by a given field.

    Args:
        page (int): Page number for pagination.
        page_size (int): Number of tasks per page.
        order_by (str): Field by which to order the tasks.

    Returns:
        dict: Paginated list of tasks in serialized format.
    """
    tasks = Task.objects.all().order_by(order_by)
    paginated_data = Paginator(tasks, page_size).get_page(page)
    tasks = TaskSerializer(paginated_data, many=True)
    return tasks.data


def retrieve_task(task_id):
    """
    Retrieve a task by its ID.

    Args:
        task_id (int): ID of the task to retrieve.

    Returns:
        Task or None: The task instance if found, otherwise None.
    """
    try:
        return Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return None


def assign_task(serializer):
    """
    Assign users to a task.

    - Updates the assigned users for a given task.

    Args:
        serializer (TaskAssignSerializer): Validated serializer with user assignments.

    Returns:
        dict: Serialized task data with updated assigned users.
    """
    task = serializer.instance
    assigned_users = serializer.validated_data.get("assigned_users", [])

    task.assigned_users.add(*assigned_users)

    return TaskAssignSerializer(task).data


def get_user_tasks(user_id):
    """
    Get user details and all assigned tasks in a single query.

    - Uses `prefetch_related` to optimize query performance.

    Args:
        user_id (int): ID of the user whose tasks need to be fetched.

    Returns:
        dict: A structured response containing user details and their assigned tasks.
    """
    user = User.objects.prefetch_related("tasks").filter(id=user_id).first()

    if not user:
        return {"error": config.USER_NOT_FOUND}

    return {
        "email": user.email,
        "name": user.get_full_name() or user.first_name,
        "tasks": UserTaskSerializer(user.tasks.all(), many=True).data,
    }

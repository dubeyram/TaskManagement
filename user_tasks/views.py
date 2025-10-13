"""
Views for the Task Management application.

This module provides API views for:
- Creating users
- Listing and creating tasks
- Assigning tasks to users
- Retrieving tasks assigned to a specific user
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .signals import user_task_assigned, create_task as create_task_signal
from .serializer import TaskSerializer, UserSerializer, TaskAssignSerializer
from .gateway import (
    create_user,
    list_tasks,
    create_task,
    retrieve_task,
    assign_task,
    get_user_tasks,
)
from task_management import config
import logging

logger = logging.getLogger(__name__)
logger.info("Logger working properly in views")


class CreateUser(APIView):
    """
    API endpoint to create a new user.

    Handles user creation, password encryption, and username generation.
    """
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = create_user(serializer)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateListTask(APIView):
    """
    API endpoint to create and list tasks.

    Supports pagination and sorting.
    """

    def get(self, request):
        """Retrieve a paginated list of tasks with sorting options."""
        page = request.GET.get("page", 1)
        page_size = request.GET.get("page_size", 10)
        order_by = request.GET.get("order_by", "id")
        tasks = list_tasks(page, page_size, order_by)

        return Response(tasks, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new task and return the serialized object."""
        try:
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                create_task(serializer)
                create_task_signal.send(
                    sender=None, task=serializer.data, extra_data={"created": True}
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            create_task_signal.send(
                sender=None, task=None, extra_data={"created": False}, error=str(e)
            )
            return Response({"error": str(e)})


class TaskAssign(APIView):
    """
    API endpoint to assign a task to users.

    Uses PATCH to update only assigned users field.
    """

    def patch(self, request, task_id):
        """Assign a task to a user and return the updated task details."""
        task = retrieve_task(task_id)

        if task:
            serializer = TaskAssignSerializer(task, data=request.data)
            if serializer.is_valid():
                assigned = assign_task(serializer)
                user_task_assigned.send(
                    sender=None,
                    task=assigned,
                    extra_data={"user_id": assigned.get("assigned_users")},
                )
                return Response(assigned, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"error": config.TASK_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND
        )


class UserTasks(APIView):
    """
    API endpoint to fetch all tasks assigned to a specific user.

    Returns structured JSON response containing user details and assigned tasks.
    """

    def get(self, request, user_id):
        """Retrieve tasks assigned to a user with structured response."""
        user_tasks = get_user_tasks(user_id)
        return Response(user_tasks, status=status.HTTP_200_OK)

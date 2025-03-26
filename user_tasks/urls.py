"""
URL configuration for the Task Management project.

This module defines URL patterns for the task management system.
It routes API requests to the appropriate views.

Routes:
- `task/` → Create a new task or retrieve a list of tasks.
- `user/` → Create a new user.
- `task/<int:task_id>/assign/` → Assign a task to users.
- `user/<int:user_id>/tasks/` → Retrieve all tasks assigned to a specific user.
"""

from django.urls import path
from user_tasks.views import CreateListTask, CreateUser, UserTasks, TaskAssign

urlpatterns = [
    path("task/", CreateListTask.as_view(), name="task_list_create"),
    path("user/", CreateUser.as_view(), name="user_create"),
    path("task/<int:task_id>/assign/", TaskAssign.as_view(), name="task_assign"),
    path("user/<int:user_id>/tasks/", UserTasks.as_view(), name="user_tasks"),
]

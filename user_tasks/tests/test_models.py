# test_models_user
import pytest
from django.db import IntegrityError
from user_tasks.models import User, Task
from django.contrib.auth import get_user_model
from user_tasks.serializer import UserSerializer
from user_tasks.gateway import create_user

User = get_user_model()

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
        username="ram",
        email="ram@",
        password="testpass123",
        first_name="Ram",
        mobile="1234567890"
    )
    assert user.username == "ram"
    assert user.email == "ram@"
    assert str(user) == "Ram" 


@pytest.mark.django_db
def test_user_unique_email():
    User.objects.create_user(
        username="ram",
        email="ram@example.com",
        password="testpass123",
    )
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username="ram2",
            email="ram@example.com",  # duplicate
            password="testpass456",
        )


@pytest.mark.django_db
def test_user_optional_mobile():
    user = User.objects.create_user(
        username="sita",
        email="sita@example.com",
        password="testpass123"
    )
    assert user.mobile is None


# test_models_task

@pytest.mark.django_db
def test_task_creation():
    task = Task.objects.create(
        name="Test Task",
        description="Task description",
        task_type="Development"
    )
    assert task.name == "Test Task"
    assert task.status == "Pending"  # default
    assert str(task) == "Test Task"  # __str__


@pytest.mark.django_db
def test_task_status_choices():
    task = Task.objects.create(
        name="Another Task",
        description="Test desc",
        task_type="Testing",
        status="Completed",
    )
    assert task.status == "Completed"


@pytest.mark.django_db
def test_task_assign_users():
    user1 = User.objects.create_user(username="ram", email="ram@example.com", password="pass123")
    user2 = User.objects.create_user(username="sita", email="sita@example.com", password="pass123")
    task = Task.objects.create(
        name="Team Task",
        description="Assigned to multiple users",
        task_type="Collaboration"
    )
    task.assigned_users.set([user1, user2])
    
    assert task.assigned_users.count() == 2
    assert user1 in task.assigned_users.all()
    assert user2 in task.assigned_users.all()


@pytest.mark.django_db
def test_create_user_gateway():
    data = {"email": "ram@example.com", "first_name": "Ram"}
    serializer = UserSerializer(data=data)
    assert serializer.is_valid()
    user = create_user(serializer)
    assert user.username.startswith("ram")
    assert user.check_password(user.password) is False  # password is hashed
    assert User.objects.filter(email="ram@example.com").exists()

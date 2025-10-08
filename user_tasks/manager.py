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


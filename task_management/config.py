import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(message)s")

DEFAULT_DATABASE = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.getenv("DATABASE_NAME"),
    "USER": os.getenv("DATABASE_USER"),
    "PASSWORD": os.getenv("DATABASE_PASSWORD"),
    "HOST": os.getenv("HOST"),
    "PORT": os.getenv("PORT"),
}

TASK_NOT_FOUND = "Task not found"
USER_NOT_FOUND = "User not found"
EMAIL_FROM = os.getenv("EMAIL_FROM")
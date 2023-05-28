from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string

CHOICES = (
    ("user", "пользователь"),
    ("moderator", "модератор"),
    ("admin", "администратор"),
)


class User(AbstractUser):
    bio = models.TextField(
        "Биография",
        blank=True,
    )
    role = models.CharField(
        "Должность",
        max_length=16,
        choices=CHOICES,
        default="user",
    )
    email = models.EmailField(unique=True, max_length=254)


class ConfirmationCode(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activation_code",
    )
    code = models.CharField(max_length=6, default=get_random_string)

    def __str__(self) -> str:
        return self.code

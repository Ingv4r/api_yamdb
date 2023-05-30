from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string


class User(AbstractUser):
    """Кастомная модель пользователя с назначением роли."""
    CHOICES = (
        ("user", "пользователь"),
        ("moderator", "модератор"),
        ("admin", "администратор"),
    )

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

    @property
    def is_admin(self):
        """Кастомный метод проверки роли админа."""
        if self.role == self.CHOICES[2][0]:
            return True

    @property
    def is_moderator(self):
        """Кастомный метод проверки роли модератора."""
        if self.role == self.CHOICES[1][0]:
            return True


class ConfirmationCode(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activation_code",
    )
    code = models.CharField(max_length=6, default=get_random_string(6))

    def __str__(self) -> str:
        return self.code

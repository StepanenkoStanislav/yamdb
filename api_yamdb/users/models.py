from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE = [('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')]


class CustomUser(AbstractUser):
    email = models.EmailField(
        blank=False,
        unique=True,
    )
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=10,
        choices=ROLE,
        default='user',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']
        unique_together = ('username', 'email')

    @property
    def is_admin(self):
        return self.role == ROLE[2][0] or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == ROLE[1][0]

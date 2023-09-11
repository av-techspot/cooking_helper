from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    """Модель кастомного пользователя"""
    username = models.CharField(
        max_length=150,
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
        null=True,
        blank=True
    )
    email = models.EmailField(('Email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписки"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ("user", "following")

    def __str__(self):
        return f'{self.user.username} - {self.following.username}'

    def clean(self):
        if self.user == self.following:
            raise ValidationError('Нельзя подписываться на самого себя')

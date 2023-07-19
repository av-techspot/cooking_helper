from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
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

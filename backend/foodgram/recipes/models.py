from django.db import models
from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='media/',
        verbose_name='Картинка'
    )
    description = models.TextField(
        max_length=255,
        verbose_name='Описание'
    )
    ingredients = models.ForeignKey(
    )
    tag = models.ForeignKey(
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (мин)'
    )

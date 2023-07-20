from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Наименование'
    )
    measurement_unit = models.CharField(
        max_length=25,
        verbose_name='Единица измерения'
    )


class Tag(models.Model):
    pass


class RecipeIngredient(models.Model):
    pass


class RecipeTag(models.Model):
    pass

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

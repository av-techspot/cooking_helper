from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Тег'
    )
    color = models.CharField(
        max_length=7,
        null=True,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        max_length=200,
        null=True,
        unique=True,
        verbose_name='Слаг'
    )


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


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество'
    )


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='tags'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

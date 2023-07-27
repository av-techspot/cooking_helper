from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class TagChoice(models.TextChoices):
    BREAKFAST = 'Завтрак'
    LUNCH = 'Обед'
    DINNER = 'Ужин'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование',
        db_index=True
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return f"{self.name} / {self.measurement_unit}"


class Tag(models.Model):
    BLUE = '#0000FF'
    ORANGE = '#FFA500'
    GREEN = '#008000'
    PURPLE = '#800080'
    YELLOW = '#FFFF00'

    COLOR_CHOICES = [
        (BLUE, 'Синий'),
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Фиолетовый'),
        (YELLOW, 'Желтый'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name='Тег',
        db_index=True
    )
    color = models.CharField(
        max_length=7,
        null=True,
        choices=COLOR_CHOICES,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        max_length=200,
        null=True,
        unique=True,
        verbose_name='Слаг'
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        db_index=True
    )
    image = models.ImageField(
        upload_to='media/',
        verbose_name='Изображение блюда'
    )
    description = models.TextField(
        max_length=255,
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes'
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(1, message='Минимальное время 1 мин'),
        ),
        verbose_name='Время приготовления (мин)'
    )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(1, message='Минимальное количество 1'),
        ),
        verbose_name='Количество',
    )


# class RecipeTag(models.Model):
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='tags'
#     )
#     tag = models.ForeignKey(
#         Tag,
#         on_delete=models.CASCADE,
#         related_name='recipes'
#     )

class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_user_favorite')
        ]


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_cart_user')
        ]

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

MAX_LENGTH = 200


class TagChoice(models.TextChoices):
    """Класс выбора тегов"""
    BREAKFAST = 'Завтрак'
    LUNCH = 'Обед'
    DINNER = 'Ужин'


class Ingredient(models.Model):
    """Модель ингредиента"""
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Наименование',
        db_index=True
    )
    measurement_unit = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Единица измерения'
    )

    def __str__(self):
        return f"{self.name} / {self.measurement_unit}"

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique ingredient')
        ]


class Tag(models.Model):
    """Модель тегов"""
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
        max_length=MAX_LENGTH,
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
        max_length=MAX_LENGTH,
        null=True,
        unique=True,
        verbose_name='Слаг'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipe(models.Model):
    """Модель рецепта"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название',
        db_index=True
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение блюда'
    )
    text = models.TextField(
        max_length=255,
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                1,
                "Минимальное время приготовления - 1 мин.",
            ),
            MaxValueValidator(
                300,
                "Время приготовления не может превышать 300 мин.",
            ),
        ),
        verbose_name='Время приготовления (мин)'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    """Связанная модель рецепта и ингредиента"""
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
            MinValueValidator(
                1,
                "Количество должно быть больше 0",
            ),
            MaxValueValidator(
                10000,
                "Количество должно быть меньше 10000",
            ),
        ),
        verbose_name='Количество',
    )

    class Meta:
        ordering = ['recipe']
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique_ingredient_recipe')
        ]

    def __str__(self) -> str:
        return f"{self.amount} {self.ingredient}"


class Favorite(models.Model):
    """Модель избранного"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite_recipe')
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'


class Cart(models.Model):
    """Модель списка покупок"""
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
        ordering = ['-id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_cart_user')
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'

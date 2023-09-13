from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Cart, Favorite, Ingredient, Recipe, RecipeIngredient, Tag


class IngredientResource(resources.ModelResource):
    """Ресурс-класс ингредиентов"""
    class Meta:
        model = Ingredient


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    """Ингредиенты в панели администратора"""
    resource_class = IngredientResource
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name', )
    search_fields = ('name', )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Рецепты в панели администратора"""
    list_display = (
        'pk',
        'name',
        'author',
        'text',
        'cooking_time',
        'in_favorites',
        'image',
    )

    search_fields = ('name', 'author__username', 'tags__name',)
    filter_horizontal = ('tags',)
    readonly_fields = ('in_favorites',)
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'

    @admin.display(description='В избранном')
    def in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Теги в панели администратора"""
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ['name', 'slug']
    empty_value_display = '-пусто-'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Связанные ингредиенты-рецепты в панели администратора"""
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    search_fields = ('ingredient__name', 'recipe__name')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Подписки в панели администратора"""
    list_display = ('pk', 'user', 'recipe')
    search_fields = ['user__username', 'user__email']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Список покупок в панели администратора"""
    list_display = ('pk', 'user', 'recipe')
    search_fields = ("user__username", "recipe__name")

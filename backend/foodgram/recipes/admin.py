from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Cart, Favorite, Ingredient, Recipe, RecipeIngredient, Tag


class IngredientResource(resources.ModelResource):
    ''' Ресурс-класс ингредиентов'''
    class Meta:
        model = Ingredient


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    '''Ингредиенты в панели администратора'''
    resource_class = IngredientResource
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    '''Рецепты в панели администратора'''
    list_display = ('name', 'author', 'favorites_number')
    list_filter = ('author', 'name', 'tag')

    def favorites_number(self, obj):
        return obj.favorites.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    '''Теги в панели администратора'''
    pass


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    '''Связанные ингредиенты-рецепты в панели администратора'''
    pass


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    '''Подписки в панели администратора'''
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    '''Список покупок в панели администратора'''
    pass

from django.contrib.auth import get_user_model
from django_filters.rest_framework import (BooleanFilter, CharFilter,
                                           FilterSet,
                                           ModelMultipleChoiceFilter)
from recipes.models import Recipe, Tag
from rest_framework.filters import SearchFilter

User = get_user_model()


class IngredientSearchFilter(SearchFilter):
    """Фильтрация поиска ингредиентов"""
    search_param = 'name'


class AuthorAndTagFilter(FilterSet):
    """Фильтр рецептов"""
    author = CharFilter()
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        label='Tags',
        to_field_name='slug'
    )
    is_favorited = BooleanFilter(method='get_favorite')
    is_in_shopping_cart = BooleanFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def get_favorite(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(cart__user=self.request.user)
        return queryset

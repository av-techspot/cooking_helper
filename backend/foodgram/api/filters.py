from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter

User = get_user_model()


class IngredientSearchFilter(SearchFilter):
    """Фильтрация поиска ингредиентов"""
    search_param = 'name'

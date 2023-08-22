from rest_framework import viewsets
from .models import Tag, Ingredient, Recipe
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .filters import IngredientSearchFilter, AuthorAndTagFilter
from .pagination import LimitPageNumberPagination


class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TagSerializer


class IngredientViewset(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPageNumberPagination
    filter_class = AuthorAndTagFilter
    permission_classes = [IsOwnerOrReadOnly]

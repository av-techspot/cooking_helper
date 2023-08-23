from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import IngredientViewset, RecipeViewset, TagViewset

router = DefaultRouter()
router.register('tags', TagViewset, basename='tags')
router.register('ingredients', IngredientViewset, basename='ingredients')
router.register('recipes', RecipeViewset, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]

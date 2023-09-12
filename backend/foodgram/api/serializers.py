# isort: skip_file
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status

import users.api.serializers as us
from foodgram.utils import (
    LOW_COOKING_LIMIT,
    LOW_INGREDIENT_LIMIT,
    is_greater_than_zero
)
from recipes.models import (
    Cart,
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag
)
from users.models import Follow, User


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов"""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор связанной модели рецепт-ингредиент"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
#       validators = [
#           UniqueTogetherValidator(
#               queryset=RecipeIngredient.objects.all(),
#               fields=['ingredient', 'recipe']
#           )
#       ]


class ReadRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор чтения рецепта"""
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = us.FoodgramUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredient',
        many=True,
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and Favorite.objects.filter(user=self.context['request'].user,
                                        recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and Cart.objects.filter(
                user=self.context['request'].user,
                recipe=obj).exists()
        )


class CreateRecipeSerializer(ReadRecipeSerializer):
    """Сериализатор создания рецепта"""
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = us.FoodgramUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredient',
        many=True,
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text',
            'cooking_time'
        )

    def validate(self, value):
        ingredients = self.initial_data.get('ingredients')
        if not value:
            raise serializers.ValidationError({
                'ingredients': 'Нужен хоть один ингридиент для рецепта'
            })
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(Ingredient,
                                           id=ingredient_item['id'])
            is_greater_than_zero(int(ingredient_item['amount']), {
                'ingredients': (f'Убедитесь, что значение количества '
                                f'ингредиента не менее'
                                f'{LOW_INGREDIENT_LIMIT}')
            })
            ingredient_list.append(ingredient)
        return value

    def validate_cooking_time(self, value):
        if not value:
            raise serializers.ValidationError({
                'cooking_time': 'Время приготовления должно быть указано'
            })
        is_greater_than_zero(int(value), {
            'cooking_time': f'Время приготовления должно '
                            f' быть бне менее {LOW_COOKING_LIMIT}'
        })
        return value

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )

    @transaction.atomic
    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = self.initial_data.get('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        RecipeIngredient.objects.filter(recipe=instance).all().delete()
        self.create_ingredients(
            self.initial_data.get('ingredients'), instance
        )
        instance.save()
        return instance


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок"""
    class Meta:
        model = Cart
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор избранного"""
    class Meta:
        model = Favorite
        fields = '__all__'


class ShortenedRecipeSerializer(serializers.ModelSerializer):
    """Сокращенный сериализатор рецепта"""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор подписок"""
    id = serializers.ReadOnlyField(source='following.id')
    email = serializers.ReadOnlyField(source='following.email')
    username = serializers.ReadOnlyField(source='following.username')
    first_name = serializers.ReadOnlyField(source='following.first_name')
    last_name = serializers.ReadOnlyField(source='following.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('__all__',)

    def validate(self, obj):
        if (self.context['request'].user == obj):
            raise serializers.ValidationError(
                detail='Вы не можете подписаться на себя',
                code=status.HTTP_400_BAD_REQUEST
            )
        return obj

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, following=obj.following
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.query_params.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.following)
        if limit:
            queryset = queryset[:int(limit)]
        return ShortenedRecipeSerializer(
            queryset,
            many=True,
            read_only=True
        ).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.following).count()

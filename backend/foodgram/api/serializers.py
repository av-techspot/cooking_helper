# isort: skip_file
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

import users.api.serializers as us
from api.utils import (
    LOW_COOKING_LIMIT,
    LOW_INGREDIENT_LIMIT,
    validate_low_limit
)
from recipes.models import (
    Cart,
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag
)
from users.models import Follow


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
        validators = [
            UniqueTogetherValidator(
                queryset=RecipeIngredient.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class ReadRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор чтения рецепта"""
    image = Base64ImageField()
    tag = TagSerializer(read_only=True, many=True)
    author = us.FoodgramUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set',
        many=True,
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tag', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if self.context.get('request') is None:
            return False
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if self.context.get('request') is None:
            return False
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(cart__user=user, id=obj.id).exists()


class CreateRecipeSerializer(ReadRecipeSerializer):
    """Сериализатор создания рецепта"""
    image = Base64ImageField()
    tag = TagSerializer(read_only=True, many=True)
    author = us.FoodgramUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set',
        many=True,
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tag', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text',
            'cooking_time'
        )

    def validate_ingredients(self, value):
        ingredients = self.initial_data.get('ingredients')
        value = ingredients
        if not value:
            raise serializers.ValidationError({
                'ingredients': 'Нужен хоть один ингридиент для рецепта'})
        ingredient_list = []
        for ingredient_item in value:
            ingredient = get_object_or_404(Ingredient,
                                           id=ingredient_item['id'])
            if ingredient in ingredient_list:
                raise serializers.ValidationError('Ингридиенты должны '
                                                  'быть уникальными')
            ingredient_list.append(ingredient)
            validate_low_limit(int(ingredient_item['amount']), {
                    'ingredients': (f'Убедитесь, что значение количества '
                                    f'ингредиента больше '
                                    f'{LOW_INGREDIENT_LIMIT}')
                })
        return value

    def validate_cooking_time(self, value):
        if not value:
            raise serializers.ValidationError({
                'cooking_time': 'Время приготовления должно быть указано'
            })
        validate_low_limit(int(value), {
                'cooking_time': f'Время приготовления должно '
                                f' быть больше {LOW_COOKING_LIMIT}'
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
        recipe.tag.set(tags_data)
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
        instance.tag.clear()
        tags_data = self.initial_data.get('tags')
        instance.tag.set(tags_data)
        RecipeIngredient.objects.filter(recipe=instance).all().delete()
        self.create_ingredients(validated_data.get('ingredients'), instance)
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
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return ShortenedRecipeSerializer(
            queryset, many=True
        ).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

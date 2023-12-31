from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import Follow, User


class FoodgramUserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания кастомного пользователя"""
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ])
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ])

    class Meta:
        model = User
        fields = (
            'email', 'id', 'password', 'username',
            'first_name', 'last_name'
        )
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class FoodgramUserSerializer(UserSerializer):
    """Сериализатор чтения кастомного пользователя"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, following=obj.id).exists()

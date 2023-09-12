from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    """Пользователь в панели администратора"""
    list_display = (
        'pk',
        'username',
        'last_name',
        'first_name',
        'email',
    )
    list_filter = (
        'username',
        'email',
        'last_name',
        'first_name',
    )
    search_fields = ('email', 'username')


@admin.register(Follow)
class AdminFollow(admin.ModelAdmin):
    """Подписки в панели администратора"""
    list_display = (
        'pk',
        'user',
        'following'
    )
    search_fields = (
        'user__username',
        'following__username'
    )
    empty_value_display = '-пусто-'

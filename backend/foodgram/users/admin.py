from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_filter = ('email', 'username',)


@admin.register(Follow)
class AdminFollow(admin.ModelAdmin):
    pass

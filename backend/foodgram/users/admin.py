from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import UserAvatar


User = get_user_model()


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(UserAvatar)
class UserAvatarAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')
    search_fields = ('user__username',)

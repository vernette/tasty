from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

from .models import CustomUser, UserAvatar
from core.serializers import Base64ImageField


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class UserAvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = UserAvatar
        fields = ('avatar',)


class CustomUserSerializer(UserSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        request = self.context.get('request')
        user_avatar = UserAvatar.objects.filter(user=obj).first()
        if user_avatar and user_avatar.avatar:
            return request.build_absolute_uri(user_avatar.avatar.url)
        return None

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('avatar',)

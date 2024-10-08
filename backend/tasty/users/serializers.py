from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated
from djoser.serializers import UserCreateSerializer, UserSerializer

from users.models import CustomUser, UserAvatar
from tasty.constants import NOT_AUTHENTICATED
from tasty.utils import Base64ImageField


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class UserAvatarSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta:
        model = UserAvatar
        fields = ('avatar',)


class BaseCustomUserSerializer(UserSerializer):
    avatar = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        request = self.context.get('request')
        if not request:
            return None

        user_avatar = getattr(obj, 'avatar', None)
        if user_avatar and user_avatar.avatar:
            return request.build_absolute_uri(user_avatar.avatar.url)
        return None

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.subscribers.filter(user=request.user).exists()
        return False

    class Meta(UserSerializer.Meta):
        model = CustomUser
        fields = UserSerializer.Meta.fields + (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar'
        )


class CustomCurrentUserSerializer(BaseCustomUserSerializer):
    class Meta(BaseCustomUserSerializer.Meta):
        fields = BaseCustomUserSerializer.Meta.fields

    def to_representation(self, instance):
        request = self.context.get('request')
        if not request.user.is_authenticated:
            raise NotAuthenticated(NOT_AUTHENTICATED)
        return super().to_representation(instance)


class CustomUserDetailSerializer(BaseCustomUserSerializer):
    class Meta(BaseCustomUserSerializer.Meta):
        fields = BaseCustomUserSerializer.Meta.fields

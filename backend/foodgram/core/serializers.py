from collections import Counter

from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from core.models import Recipe, RecipeIngredient, Ingredient, Tag
from users.models import UserAvatar
from foodgram.constants import (
    INGREDIENTS_DATA_REQUIRED, TAGS_DATA_REQUIRED, AMOUNT_REQUIRED,
    COOKING_TIME_REQUIRED, INGREDIENT_DUPLICATES, TAG_DUPLICATES,
    INGREDIENT_DOES_NOT_EXIST, TAG_DOES_NOT_EXIST, NOT_AUTHENTICATED,
    MIN_AMOUNT, MAX_AMOUNT, MIN_AMOUNT_ERROR, MAX_AMOUNT_ERROR,
    MIN_COOKING_TIME, MAX_COOKING_TIME, MIN_COOKING_TIME_ERROR,
    MAX_COOKING_TIME_ERROR
)
from foodgram.utils import Base64ImageField
from users.serializers import BaseCustomUserSerializer


User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField(
        validators=[
            MinValueValidator(
                MIN_AMOUNT,
                message=MIN_AMOUNT_ERROR
            ),
            MaxValueValidator(
                MAX_AMOUNT,
                message=MAX_AMOUNT_ERROR
            )
        ]
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAvatar
        fields = ('avatar',)


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredients',
        many=True,
        read_only=True
    )
    author = BaseCustomUserSerializer(read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    cooking_time = serializers.IntegerField(
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME,
                message=MIN_COOKING_TIME_ERROR
            ),
            MaxValueValidator(
                MAX_COOKING_TIME,
                message=MAX_COOKING_TIME_ERROR
            )
        ]
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def validate(self, attrs):
        ingredients_data = self.context['request'].data.get('ingredients')
        tags_data = self.context['request'].data.get('tags')
        self.validate_ingredients(ingredients_data)
        self.validate_tags(tags_data)
        return attrs

    def validate_ingredients(self, ingredients_data):
        if not ingredients_data:
            raise serializers.ValidationError(INGREDIENTS_DATA_REQUIRED)

        ingredient_ids = [ingredient['id'] for ingredient in ingredients_data]
        duplicate_ingredients = [
            id for id, count in Counter(ingredient_ids).items() if count > 1
        ]
        if duplicate_ingredients:
            raise serializers.ValidationError(
                INGREDIENT_DUPLICATES.format(
                    ', '.join(map(str, duplicate_ingredients))
                )
            )

        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            if not Ingredient.objects.filter(id=ingredient_id).exists():
                raise serializers.ValidationError(
                    INGREDIENT_DOES_NOT_EXIST.format(
                        ingredient_id=ingredient_id
                    )
                )

    def validate_tags(self, tags_data):
        if not tags_data:
            raise serializers.ValidationError(TAGS_DATA_REQUIRED)

        duplicate_tags = [
            id for id, count in Counter(tags_data).items() if count > 1
        ]
        if duplicate_tags:
            raise serializers.ValidationError(
                TAG_DUPLICATES.format(
                    ', '.join(map(str, duplicate_tags))
                )
            )

        for tag_id in tags_data:
            if not Tag.objects.filter(id=tag_id).exists():
                raise serializers.ValidationError(
                    TAG_DOES_NOT_EXIST.format(tag_id=tag_id)
                )

    def create(self, validated_data):
        request = self.context.get('request')
        tags_data = request.data.get('tags')
        ingredients_data = request.data.get('ingredients')

        validated_data.pop('recipe_ingredients', None)

        if not request.user.is_authenticated:
            raise AuthenticationFailed(NOT_AUTHENTICATED)

        validated_data['author'] = request.user

        with transaction.atomic():
            recipe = super().create(validated_data)

            if tags_data:
                tags = Tag.objects.filter(id__in=tags_data)
                recipe.tags.set(tags)

            recipe_ingredients = [
                RecipeIngredient(
                    recipe=recipe,
                    ingredient_id=ingredient_data['id'],
                    amount=ingredient_data['amount']
                )
                for ingredient_data in ingredients_data
            ]
            RecipeIngredient.objects.bulk_create(recipe_ingredients)

        return recipe

    def update(self, instance, validated_data):
        request = self.context.get('request')
        tags_data = request.data.get('tags')
        ingredients_data = request.data.get('ingredients')
        validated_data.pop('ingredients', None)
        instance = super().update(instance, validated_data)

        with transaction.atomic():
            instance.recipe_ingredients.all().delete()

            if tags_data:
                tags = Tag.objects.filter(id__in=tags_data)
                instance.tags.set(tags)

            recipe_ingredients = [
                RecipeIngredient(
                    recipe=instance,
                    ingredient_id=ingredient_data['id'],
                    amount=ingredient_data['amount']
                )
                for ingredient_data in ingredients_data
            ]
            RecipeIngredient.objects.bulk_create(recipe_ingredients)

        return instance

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.favorites.filter(user=user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.in_shopping_cart.filter(user=user).exists()
        return False

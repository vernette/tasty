from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from core.models import Recipe, RecipeIngredient, Ingredient, Tag
from users.models import UserAvatar
from tasty.constants import (
    INGREDIENTS_DATA_REQUIRED, TAGS_DATA_REQUIRED, INGREDIENT_DUPLICATES,
    TAG_DUPLICATES, INGREDIENT_DOES_NOT_EXIST, TAG_DOES_NOT_EXIST,
    NOT_AUTHENTICATED, MIN_AMOUNT, MAX_AMOUNT, MIN_AMOUNT_ERROR,
    MAX_AMOUNT_ERROR, MIN_COOKING_TIME, MAX_COOKING_TIME,
    MIN_COOKING_TIME_ERROR, MAX_COOKING_TIME_ERROR
)
from tasty.utils import Base64ImageField
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

        ingredient_ids = set()
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data['id']
            if ingredient_id in ingredient_ids:
                raise serializers.ValidationError(
                    INGREDIENT_DUPLICATES.format(ingredient_id)
                )
            if not Ingredient.objects.filter(id=ingredient_id).exists():
                raise serializers.ValidationError(
                    INGREDIENT_DOES_NOT_EXIST.format(ingredient_id)
                )
            ingredient_ids.add(ingredient_id)

    def validate_tags(self, tags_data):
        if not tags_data:
            raise serializers.ValidationError(TAGS_DATA_REQUIRED)

        tag_ids = set()
        for tag_id in tags_data:
            if tag_id in tag_ids:
                raise serializers.ValidationError(
                    TAG_DUPLICATES.format(tag_id)
                )
            if not Tag.objects.filter(id=tag_id).exists():
                raise serializers.ValidationError(
                    TAG_DOES_NOT_EXIST.format(tag_id)
                )
            tag_ids.add(tag_id)

    def create(self, validated_data):
        request = self.context.get('request')
        ingredients_data = request.data.get('ingredients')
        validated_data.pop('recipe_ingredients', None)

        if not request.user.is_authenticated:
            raise AuthenticationFailed(NOT_AUTHENTICATED)

        validated_data['author'] = request.user
        return self.save_recipe(validated_data, ingredients_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        ingredients_data = request.data.get('ingredients')
        validated_data.pop('ingredients', None)
        instance = super().update(instance, validated_data)
        return self.save_recipe(validated_data, ingredients_data, instance)

    def save_recipe(self, validated_data, ingredients_data, instance=None):
        with transaction.atomic():
            if instance:
                instance.recipe_ingredients.all().delete()

            recipe = (
                super().create(validated_data)
                if not instance else instance
            )

            if ingredients_data:
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

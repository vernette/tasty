from collections import Counter

from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models import Recipe, RecipeIngredient, Ingredient, Tag
from users.models import UserAvatar
from .utils import Base64ImageField
from users.serializers import BaseCustomUserSerializer


User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')
    amount = serializers.IntegerField()

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
    ingredients = RecipeIngredientSerializer(source='recipe_ingredients', many=True, read_only=True)
    author = BaseCustomUserSerializer(read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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
        if not ingredients_data:
            raise serializers.ValidationError("Ingredients data is required.")

        ingredient_ids = [ingredient['id'] for ingredient in ingredients_data]
        duplicate_ingredients = [id for id, count in Counter(ingredient_ids).items() if count > 1]
        if duplicate_ingredients:
            raise serializers.ValidationError(
                f"Duplicate ingredients found: {', '.join(map(str, duplicate_ingredients))}")

        tags_data = self.context['request'].data.get('tags')
        if not tags_data:
            raise serializers.ValidationError("Tags data is required.")

        duplicate_tags = [id for id, count in Counter(tags_data).items() if count > 1]
        if duplicate_tags:
            raise serializers.ValidationError(
                f"Duplicate tags found: {', '.join(map(str, duplicate_tags))}")

        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            if not Ingredient.objects.filter(id=ingredient_id).exists():
                raise serializers.ValidationError(
                    f"Ingredient with id {ingredient_id} does not exist.")

        for tag_id in tags_data:
            if not Tag.objects.filter(id=tag_id).exists():
                raise serializers.ValidationError(
                    f"Tag with id {tag_id} does not exist.")

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        tags_data = request.data.get('tags')
        ingredients_data = request.data.get('ingredients')

        validated_data.pop('recipe_ingredients', None)
        validated_data['author'] = request.user

        recipe = super().create(validated_data)

        if tags_data:
            tags = Tag.objects.filter(id__in=tags_data)
            recipe.tags.set(tags)

        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            amount = ingredient_data.get('amount')
            ingredient = Ingredient.objects.get(id=ingredient_id)
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, amount=amount,
                                            measurement_unit=ingredient.measurement_unit)

        return recipe

    def update(self, instance, validated_data):
        request = self.context.get('request')
        tags_data = request.data.get('tags')
        ingredients_data = request.data.get('ingredients')

        validated_data.pop('ingredients', None)
        instance = super().update(instance, validated_data)

        if ingredients_data is None:
            raise serializers.ValidationError("Ingredients data is required.")

        if tags_data:
            tags = Tag.objects.filter(id__in=tags_data)
            instance.tags.set(tags)

        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            amount = ingredient_data.get('amount')
            ingredient = Ingredient.objects.get(id=ingredient_id)
            RecipeIngredient.objects.create(
                recipe=instance,
                ingredient=ingredient,
                amount=amount,
                measurement_unit=ingredient.measurement_unit
            )

        return instance

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.favorites.filter(user=user).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.in_shopping_carts.filter(user=user).exists()
        return False

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from tasty.constants import (
    NAME_MAX_LENGTH, MEASUREMENT_UNIT_MAX_LENGTH, MIN_COOKING_TIME,
    MAX_COOKING_TIME, MIN_COOKING_TIME_ERROR, MAX_COOKING_TIME_ERROR,
    MIN_AMOUNT, MAX_AMOUNT, MIN_AMOUNT_ERROR, MAX_AMOUNT_ERROR
)


User = get_user_model()


class BaseModel(models.Model):
    name = models.CharField(
        'Название',
        max_length=NAME_MAX_LENGTH
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Recipe(BaseModel):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/images',
        null=False,
    )
    text = models.TextField(
        verbose_name='Описание',
        null=False
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        verbose_name='Ингредиенты',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Теги',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
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
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Ingredient(BaseModel):
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=MEASUREMENT_UNIT_MAX_LENGTH
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
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
        default_related_name = 'recipe_ingredients'
        unique_together = ['recipe', 'ingredient']


class Tag(BaseModel):
    slug = models.SlugField(
        'Слаг',
        unique=True
    )

    class Meta:
        ordering = ['-id']
        unique_together = ('name', 'slug')
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class BaseModel(models.Model):
    name = models.CharField(
        'Название',
        max_length=256
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


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
    cooking_time = models.PositiveSmallIntegerField('Время приготовления')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Ingredient(BaseModel):
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=64  # TODO Change max_length later
    )

    class Meta:
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
    amount = models.PositiveSmallIntegerField('Количество')

    class Meta:
        default_related_name = 'recipe_ingredients'
        unique_together = ['recipe', 'ingredient']


class Tag(BaseModel):
    slug = models.SlugField(
        'Слаг',
        unique=True
    )

    class Meta:
        unique_together = ('name', 'slug')
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class BaseModel(models.Model):
    name = models.CharField(
        max_length=256
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Recipe(BaseModel):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='recipes/images',
        null=False,
    )
    text = models.TextField(
        null=False
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='recipes'
    )
    cooking_time = models.IntegerField(
        null=False
    )

    class Meta:
        ordering = ['-id']


class Ingredient(BaseModel):
    measurement_unit = models.CharField(
        max_length=64  # TODO Change max_length later
    )


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE
    )
    amount = models.FloatField(
        null=False
    )
    measurement_unit = models.CharField(
        max_length=64  # TODO Change max_length later
    )

    class Meta:
        default_related_name = 'recipe_ingredients'
        unique_together = ['recipe', 'ingredient']


class Tag(BaseModel):
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        unique_together = ('name', 'slug')

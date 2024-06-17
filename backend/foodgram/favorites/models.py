from django.contrib.auth import get_user_model
from django.db import models

from core.models import Recipe


User = get_user_model()


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='favorites',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='favorites',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['-id']
        unique_together = ('user', 'recipe')

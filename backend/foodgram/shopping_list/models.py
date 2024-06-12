from django.contrib.auth import get_user_model
from django.db import models

from core.models import Recipe


User = get_user_model()


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        related_name='shopping_cart',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='in_shopping_cart',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user', 'recipe')

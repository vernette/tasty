from django.conf import settings
from django.db import models


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='subscribers'
    )

    class Meta:
        ordering = ['-id']
        unique_together = ('user', 'author')

    def __str__(self):
        return f'{self.user} - {self.author}'

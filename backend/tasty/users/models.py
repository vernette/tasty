from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(
        'Имя',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150
    )
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class UserAvatar(models.Model):
    user = models.OneToOneField(
        CustomUser,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='avatar'
    )
    avatar = models.ImageField(
        'Файл аватара',
        upload_to='users/avatars',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Аватар'
        verbose_name_plural = 'Аватары'

    def __str__(self):
        return f'{self.user} - {self.avatar}'

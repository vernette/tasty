from django.db import models
from django.contrib.auth.models import AbstractUser


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

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(verbose_name='Электронная почта', max_length=254)
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150)
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=150)

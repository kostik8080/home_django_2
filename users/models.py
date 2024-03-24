from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    avatar = models.ImageField(upload_to='users/', default='users/pixlr-bg-result_9.png', **NULLABLE, verbose_name='Аватар')
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name='Телефон')
    country = models.CharField(max_length=100, **NULLABLE, verbose_name='Страна')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

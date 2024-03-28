from django.db import models
from django.utils import timezone

from users.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    def __str__(self):
        return f'{self.name} ({self.description})'

    class Meta:
        verbose_name = 'катекория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    PUBLISHED = 'Опубликовано'
    UNPUBLISHED = 'Не опубликовано'
    STATUS_CHOICES = [(PUBLISHED, 'published'), (UNPUBLISHED, 'unpublished')]


    name = models.CharField(max_length=250, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='catalog/', null=True, blank=True, verbose_name='Изоброжение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена за покупку')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата изменения')
    is_published = models.CharField(choices=STATUS_CHOICES, max_length=20, default=UNPUBLISHED, verbose_name='Статус')

    users = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Пользователь', null=True, blank=True, default=None)



    def __str__(self):
        return f'{self.name} {self.description} {self.photo} {self.category} {self.price} {self.created_at} {self.updated_at}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

        permissions = [
            (
                'set_is_published',
                'can publish product',
            ),
            (
                'change_discription',
                'can change product description',
            ),
            (
                'change_category',
                'can change product category',
            )

        ]

class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    number_version = models.PositiveIntegerField(verbose_name='Номер версии')
    name_version = models.CharField(max_length=250, verbose_name='Название версии')
    current_version = models.BooleanField(default=True, verbose_name='Текущая версия')

    def __str__(self):
        return f'{self.product} {self.number_version} {self.name_version}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
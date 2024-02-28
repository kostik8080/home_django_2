from django.db import models
from django.utils import timezone


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
    name = models.CharField(max_length=250, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='catalog/', null=True, blank=True, verbose_name='Изоброжение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена за покупку')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата изменения')



    def __str__(self):
        return f'{self.name} {self.description} {self.photo} {self.category} {self.price} {self.created_at} {self.updated_at}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'




class Blog(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)
    content = models.TextField(verbose_name='Содержимое')
    photo = models.ImageField(null=True, blank=True, verbose_name='Превью', upload_to='blog/')
    created_at = models.DateField(auto_now=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Статус публикации')
    count_views = models.IntegerField(verbose_name='Количество просмотров', default=0)

    def __str__(self):
        return f"{self.title} {self.created_at}"

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

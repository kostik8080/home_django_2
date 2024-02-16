from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    def __str__(self):
        return 'Здесь будет модель Category'

    class Meta:
        pass

class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='catalog/', null=True, blank=True, verbose_name='Изоброжение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена за покупку')
    created_at = models.DateField(verbose_name='Дата создания')
    updated_at = models.DateField(verbose_name='Дата изменения')
    def __str__(self):
        return 'Здесь будет модель Product'

    class Meta:
        pass




from django.db import models

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

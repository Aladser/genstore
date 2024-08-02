from django.db import models
from config.settings import NULLABLE


class Blog(models.Model):
    name = models.CharField(verbose_name='Заголовок', max_length=100, unique=True)
    slug = models.CharField(verbose_name='slug', max_length=100, unique=True)
    content = models.TextField(verbose_name='Содержание', default='')
    preview_image = models.ImageField(verbose_name='Изображение', upload_to='img/products', **NULLABLE)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    is_published = models.BooleanField(verbose_name='Опубликован', default=False)
    views_count = models.IntegerField(verbose_name='Число просмотров', default=0)

    def __str__(self):
        return f"{self.name}{' (опубликован)' if self.is_published else ''}. Создан {self.created_at}, число просмотров - {self.views_count}"

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ('name', 'created_at', 'views_count')
        permissions = [
            ('set_publication', 'Установить статус публикации')
        ]

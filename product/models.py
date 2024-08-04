from django.db import models
from authen.models import User
from config.settings import NULLABLE
from libs.truncate_table_mixin import TruncateTableMixin


class Category(TruncateTableMixin, models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    description = models.CharField(max_length=256, verbose_name='Описание', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Product(TruncateTableMixin, models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    is_published = models.BooleanField(verbose_name='Опубликован', default=False)
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    ava = models.ImageField(upload_to='img/products', verbose_name='Аватар', default=None, **NULLABLE)
    price = models.IntegerField(verbose_name='Цена за покупку', **NULLABLE)
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='категория',
    )
    creator = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='создатель',
        **NULLABLE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    manufactured_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата производства')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return self.name

    def current_version(self):
        return self.product_version.filter(is_current=True).first()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('name', 'price', 'created_at', 'updated_at')
        permissions = [
            ('cancel_publication', 'Отменить публикацию'),
            ('edit_description', 'Изменить описание'),
            ('edit_category', 'Изменить категорию')
        ]


class ProductVersion(TruncateTableMixin, models.Model):
    name = models.CharField(verbose_name="Название", max_length=256, default="стандарт")
    number = models.PositiveIntegerField(verbose_name="Номер")
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="product_version",
        verbose_name="продукт",
    )
    is_current = models.BooleanField(verbose_name="Текущая версия", default=False)

    class Meta:
        verbose_name = "Версия товара"
        verbose_name_plural = "Версии товара"
        ordering = ('-number',)

    def __str__(self):
        return f"{self.name} {self.number}"

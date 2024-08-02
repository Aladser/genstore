from django.contrib import admin
from product.models import *


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'creator', 'category', 'is_published')
    search_fields = ('name', 'description')


@admin.register(ProductVersion)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'number', 'name', 'is_current')

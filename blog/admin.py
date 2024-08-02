from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'views_count', 'created_at', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('name', 'slug')


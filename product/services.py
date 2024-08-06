from django.core.cache import cache

from product.models import Category


def get_categories_from_cache():
    """Возвращает список категорий из кэша"""

    category_list = cache.get('category_list')
    if category_list is None:
        category_list = Category.objects.all()
        cache.set('category_list', category_list)

    return category_list

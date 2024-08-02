from django.core.management import BaseCommand

from blog.models import Blog
from product.models import Category, Product, ProductVersion


class Command(BaseCommand):
    # Категории
    category_list = [
        {'name': 'автомобили'},
        {'name': 'бытовая химия'},
        {'name': 'продукты'},
    ]

    # Товары
    product_list = [
        {
            'name': 'Жигули',
            'category_id': 1,
            'description': 'советский автомобиль',
            'price': 1000
        },
        {
            'name': 'Мерседес',
            'category_id': 1,
            'description': 'немецкий автомобиль',
            'price': 2000
        },
        {
            'name': 'Toyota',
            'category_id': 1,
            'description': 'японский автомобиль',
            'price': 300,
            'ava': 'img/products/toyota.jpeg'
        },
        {
            'name': 'Шампунь',
            'category_id': 2,
            'description': 'для головы',
            'price': 300,
            'ava': 'img/products/shampoo.jpeg'
        },
        {
            'name': 'Мыло',
            'category_id': 2,
            'description': 'для всего тела',
            'price': 100,
            'ava': 'img/products/soap.jpeg'
        },
        {
            'name': 'Крем',
            'category_id': 2,
            'description': 'для кожи',
            'price': 200,
            'ava': 'img/products/cream.jpeg'
        },
        {
            'name': 'Хлеб',
            'category_id': 3,
            'description': 'всему голова',
            'price': 50,
            'ava': 'img/products/bread.png'
        },
    ]

    def handle(self, *args, **kwargs):
        ProductVersion.truncate()
        Product.truncate()
        Category.truncate()

        category_create_list = [Category(**ctg) for ctg in self.category_list]
        Category.objects.bulk_create(category_create_list)

        product_create_list = [Product(**prd) for prd in self.product_list]
        Product.objects.bulk_create(product_create_list)

        # блоги
        blog_list = []
        for i in range(5):
            name = f"Блог {i + 1}"
            blog_list.append({'name': name, 'slug': f"blog_{i + 1}", 'content': ' '.join([name] * 5)})

        Blog.objects.all().delete()
        blog_create_list = [Blog(**blog) for blog in blog_list]
        Blog.objects.bulk_create(blog_create_list)

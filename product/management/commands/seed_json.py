import json

from django.core.management import BaseCommand

from product.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_data():
        """получает данные из JSON файла"""
        data = {'categories': [], 'products': []}

        with open('data.json', 'r', encoding='utf8') as file:
            file_data = json.load(file)

        for elem in file_data:
            if elem['model'] == 'product.category':
                data['categories'].append({'pk': elem['pk'], 'name': elem['fields']['name']})
            else:
                data['products'].append({'name': elem['fields']['name'], 'category_id': elem['fields']['category']})
        return data

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Category.objects.all().delete()

        json_data = self.json_read_data()

        ctg_obj_list = [Category(**ctg) for ctg in json_data['categories']]
        Category.objects.bulk_create(ctg_obj_list)
        prd_obj_list = [Product(**prd) for prd in json_data['products']]
        Product.objects.bulk_create(prd_obj_list)

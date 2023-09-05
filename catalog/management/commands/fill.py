import json

from django.core.management import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    @staticmethod
    def load_data(file) -> list:
        """Парсит данные из файла data.json,
        возвращает два списка (товаров и категория)
        для последующей выгрузки в БД в функции handle"""

        categories_lst = []
        products_lst = []
        with open(file, 'r', encoding='utf-8') as f:
            file_items = json.load(f)
            for item in file_items:
                if item['model'] == "catalog.category":
                    new_category = {
                        'title': item['fields']['title'],
                        'pk': item['pk'],
                        'description': item['fields']['description']
                    }
                    categories_lst.append(Category(**new_category))
                if item['model'] == "catalog.product":
                    new_product = {
                        'title': item['fields']['title'],
                        'description': item['fields']['description'],
                        'pic': item['fields']['pic'],
                        'price': item['fields']['price'],
                        'created_at': item['fields']['create_date'],
                        'updated_at': item['fields']['change_date'],
                        'category': Category(item['fields']['category'])
                    }
                    products_lst.append(Product(**new_product))
        return [categories_lst, products_lst]

    @staticmethod
    def delete_all() -> None:
        """Удаляет все категории в БД. Все товары удаляются каскадом"""
        Category.objects.all().delete()
        # Product.objects.all().delete()

    def handle(self, *args, **kwargs):
        """Удалает все данные из БД,
        подгружает категории в БД
        подгружает товары в БД"""

        Command.delete_all()

        categories = Command.load_data('data.json')[0]
        Category.objects.bulk_create(categories)

        products = Command.load_data('data.json')[1]
        Product.objects.bulk_create(products)

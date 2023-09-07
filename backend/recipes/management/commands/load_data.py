import json

from django.core.management import BaseCommand

from config.settings import BASE_DIR
from recipes.models import Ingredient

file_path = f'{BASE_DIR}/data/ingredients.json'


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(file_path, mode='r+', encoding='utf-8') as json_file:
            ingredients = json.load(json_file)
            try:
                Ingredient.objects.bulk_create(
                    Ingredient(**data) for data in ingredients
                )
            except Exception as error:
                print(f'Произошла ошибка {error}')

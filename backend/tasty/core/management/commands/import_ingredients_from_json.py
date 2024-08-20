import os
import json

from django.core.management.base import BaseCommand, CommandError

from core.models import Ingredient
from tasty.constants import (
    IMPORT_INGREDIENTS_FROM_JSON, JSON_INVALID, FILE_PATH,
    IMPORT_SUCCESS, INGREDIENT_EXISTS, FILE_DOES_NOT_EXIST
)


class Command(BaseCommand):
    help = IMPORT_INGREDIENTS_FROM_JSON

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help=FILE_PATH)

    def handle(self, *args, **options):
        file_path = options['file_path']

        if not os.path.exists(file_path):
            raise CommandError(
                FILE_DOES_NOT_EXIST.format(file_path=file_path)
            )

        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                ingredients_data = json.load(file)
            except json.JSONDecodeError:
                raise CommandError(JSON_INVALID.format(file_path=file_path))

        for ingredient_data in ingredients_data:
            name = ingredient_data.get('name')
            measurement_unit = ingredient_data.get('measurement_unit')

            ingredient, created = Ingredient.objects.get_or_create(
                name=name,
                defaults={'measurement_unit': measurement_unit}
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        IMPORT_SUCCESS.format(name=name)
                    )
                )
                continue
            self.stdout.write(
                self.style.WARNING(
                    INGREDIENT_EXISTS.format(name=name)
                )
            )

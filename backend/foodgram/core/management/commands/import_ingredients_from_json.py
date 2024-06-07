import os
import json

from django.core.management.base import BaseCommand, CommandError

from core.models import Ingredient


class Command(BaseCommand):
    help = 'Import ingredients from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file containing ingredients')

    def handle(self, *args, **options):
        file_path = options['file_path']

        if not os.path.exists(file_path):
            raise CommandError(f"File '{file_path}' does not exist")

        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                ingredients_data = json.load(file)
            except json.JSONDecodeError:
                raise CommandError(f"File '{file_path}' is not a valid JSON file")

        for ingredient_data in ingredients_data:
            name = ingredient_data.get('name')
            measurement_unit = ingredient_data.get('measurement_unit')

            if not name or not measurement_unit:
                self.stdout.write(
                    self.style.WARNING(f"Skipping invalid ingredient: {ingredient_data}"))
                continue

            ingredient, created = Ingredient.objects.get_or_create(
                name=name,
                defaults={'measurement_unit': measurement_unit}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Ingredient '{name}' created successfully"))
                continue
            self.stdout.write(self.style.WARNING(f"Ingredient '{name}' already exists"))
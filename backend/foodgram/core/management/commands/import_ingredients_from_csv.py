import os
import csv

from django.core.management.base import BaseCommand, CommandError

from core.models import Ingredient


class Command(BaseCommand):
    help = 'Import ingredients from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file containing ingredients')

    def handle(self, *args, **options):
        file_path = options['file_path']

        if not os.path.exists(file_path):
            raise CommandError(f"File '{file_path}' does not exist")

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 2:
                    self.stdout.write(self.style.WARNING(f"Skipping invalid row: {row}"))
                    continue

                name, measurement_unit = row
                ingredient, created = Ingredient.objects.get_or_create(
                    name=name,
                    defaults={'measurement_unit': measurement_unit}
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Ingredient '{name}' created successfully"))
                    continue
                self.stdout.write(self.style.WARNING(f"Ingredient '{name}' already exists"))
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import ingredients from JSON file'

    def handle(self, *args, **options):
        pass
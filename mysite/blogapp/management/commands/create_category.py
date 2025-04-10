from django.core.management import BaseCommand
from django.db import transaction

from blogapp.models import Category
from faker import Faker


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create a new Category")
        category_name = Faker().text(max_nb_chars=10)[:-1]
        category, created = Category.objects.get_or_create(
            name=category_name,
        )
        self.stdout.write(f"Category {category.name} was created")

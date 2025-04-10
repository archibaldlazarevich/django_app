from django.core.management import BaseCommand
from django.db import transaction

from blogapp.models import Author
from faker import Faker


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create a new Author")
        author_info = [Faker().name(), "Bio"]
        author, created = Author.objects.get_or_create(
            name=author_info[0],
            bio=author_info[1],
        )
        self.stdout.write(f"Author {author.name} was created")

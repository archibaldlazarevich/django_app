from django.core.management import BaseCommand
from django.db import transaction

from blogapp.models import Tag
from faker import Faker


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create a new Tag")
        tag_name = Faker().text(max_nb_chars=10)[:-1]
        tag, created = Tag.objects.get_or_create(
            name=tag_name,
        )
        self.stdout.write(f"Tag {tag.name} was created")

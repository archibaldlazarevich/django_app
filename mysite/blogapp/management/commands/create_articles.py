from typing import Sequence

from django.core.management import BaseCommand
from django.db import transaction

from blogapp.models import Article, Author, Tag, Category
from faker import Faker

faker = Faker()


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Create a new articles")
        author, created = Author.objects.get_or_create(
            name="Author", bio="Bio"
        )
        category, created = Category.objects.get_or_create(name="Category")
        tags: Sequence[Tag] = Tag.objects.only("id").all()
        article, created = Article.objects.get_or_create(
            title=faker.text(max_nb_chars=50)[:-1],
            content=faker.text(max_nb_chars=1000),
            author=author,
            category=category,
        )
        self.stdout.write(f"\n\n\n\n{tags}\n\n\n")
        for tag in tags:
            article.tags.add(tag)
        article.save()
        # self.stdout.write(f"Created a new article {article}")

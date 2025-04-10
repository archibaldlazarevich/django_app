from django.core.management import BaseCommand
from shopapp.models import Product
import random


class Command(BaseCommand):
    """
    Creates products
    """

    def handle(self, *args, **options):
        self.stdout.write("Create products")

        products_name = [
            "Laptop",
            "Desktop",
            "Smartphone",
            "Potato",
            "Pencil",
            "Book",
        ]
        for product_name in products_name:
            product, created = Product.objects.get_or_create(
                name=product_name,
                price=random.randint(12154, 164384),
                discount=random.randint(10, 50),
            )
            self.stdout.write(f"Created product {product.name}")

        self.stdout.write(self.style.SUCCESS("Products create"))

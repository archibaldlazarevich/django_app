from django.core.management import BaseCommand

from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        orders = Order.objects.all()
        if not Order:
            self.stdout.write("no order found")
            return
        products = Product.objects.all()
        for order in orders:
            for product in products:
                order.products.add(product)

            order.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully added products {order.products.all()}"
                    f" to order {order}"
                )
            )

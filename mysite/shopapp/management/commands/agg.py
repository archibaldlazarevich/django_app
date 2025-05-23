from django.core.management import BaseCommand
from django.db.models import Count, Sum

from shopapp.models import Order


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Start demo select aggregate")
        # result = Product.objects.filter(
        #     name__contains = 'Smartphone',
        # ).aggregate(
        #     Avg('price'),
        #     Max('price'),
        #     min_price=Min('price'),
        #     count=Count('price'),
        # )
        # print(result)

        orders = Order.objects.annotate(
            total=Sum("products__price"),
            products_count=Count("products"),
        )
        for order in orders:
            print(
                f"Order #{order.id} "
                f"with {order.products_count} "
                f"products worth {order.total}"
            )
        self.stdout.write("Done")

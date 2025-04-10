from csv import DictReader
from io import TextIOWrapper

from django.contrib.auth.models import User

from shopapp.models import Product, Order


def save_csv_products(file, encoding, request):
    csv_file = TextIOWrapper(file, encoding=encoding)
    reader = DictReader(csv_file)

    products = [Product(created_by=request.user, **row) for row in reader]
    Product.objects.bulk_create(products)
    return products


def save_csv_orders(file, encoding, request):
    csv_file = TextIOWrapper(file, encoding=encoding)
    reader = DictReader(csv_file)
    orders = []
    products_to_add = []

    for row in reader:
        product_ids = [int(pk) for pk in row["products"].split(",")]
        order = Order(
            user=request.user,
            delivery_address=row.get("delivery_address", ""),
            promocode=row.get("promocode", ""),
        )
        orders.append(order)
        products_to_add.append(product_ids)
    created_orders = Order.objects.bulk_create(orders)
    for order, product_ids in zip(created_orders, products_to_add):
        products = Product.objects.filter(pk__in=product_ids)
        order.products.set(products)
    return created_orders

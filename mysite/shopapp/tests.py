from string import ascii_letters
from random import choices

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Product, Order


class ProductCreateViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username="user_test", password="password"
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        permission = Permission.objects.get(codename="add_product")
        self.user.user_permissions.add(permission)
        self.client.force_login(self.user)
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "Good table",
                "discount": "10",
            },
        )
        self.assertRedirects(response, reverse("shopapp:products_list"))


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username="user_test", password="password"
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        permission = Permission.objects.get(codename="view_order")
        self.user.user_permissions.add(permission)
        self.client.force_login(self.user)
        self.order_address = "".join(choices(ascii_letters, k=10))
        self.order = Order.objects.create(
            delivery_address=self.order_address, user=self.user, promocode=125
        )

    def tearDown(self):
        Order.objects.filter(
            delivery_address=self.order.delivery_address
        ).delete()

    def test_order_details(self):
        response = self.client.get(
            reverse("shopapp:order_details", kwargs={"pk": self.order.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertTrue(Order.objects.filter(pk=self.order.pk).exists())


class OrdersExportTestCase(TestCase):
    fixtures = [
        "orders-fixtures.json",
        "products-fixtures.json",
        "user-fixtures.json",
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="user_test", password="password"
        )
        content_type = ContentType.objects.get_for_model(Order)
        permission = Permission.objects.create(
            codename="is_staff", name="Staff", content_type=content_type
        )
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def setUp(self):
        self.client.force_login(self.user)

    def test_get_orders_view(self):

        response = self.client.get(
            reverse("shopapp:orders_export"),
        )
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "user": order.user.pk,
                "promocode": order.promocode,
                "products": [
                    product.pk for product in order.products.iterator()
                ],
            }
            for order in orders
        ]
        product_data = response.json()
        self.assertEqual(product_data["orders"], expected_data)

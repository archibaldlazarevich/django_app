"""
В этом модуле лежат различные наборы представлений.

Разные view интернет-магазина: по товарам, заказам и т.д.
"""

import logging

from timeit import default_timer
from django.core.cache import cache

from django.contrib.syndication.views import Feed
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseRedirect,
    JsonResponse,
    Http404,
)
from django.shortcuts import (
    render,
    redirect,
    reverse, get_object_or_404,
)
from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.models import Group, User
# from django.views.decorators.cache import cache_page
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)

from .forms import ProductForm, GroupForm
from .models import Product, Order, ProductImage
from .serializers import OrderSerializer

logger = logging.getLogger(__name__)


class LatestProductsFeed(Feed):
    title = "Shop products (latest)"
    description = "Updates on changes on products"
    link = reverse_lazy("shopapp:products_list")

    def items(self):
        return Product.objects.filter(archived__isnull=False).order_by(
            "-created_at"
        )[:5]

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:100]


class ShopIndexView(View):

    # @method_decorator(cache_page(5))
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ("Laptop", 1999),
            ("Desktop", 2999),
            ("Smartphone", 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
            "items": 1,
        }
        # logger.debug("Products for shop index: %s", products)
        # logger.info("Rendering shop index")
        print("shop index context", context)
        return render(request, "shopapp/shop-index.html", context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest):
        context = {
            "form": GroupForm,
            "groups": Group.objects.prefetch_related("permissions").all(),
        }
        return render(request, "shopapp/groups-list.html", context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = "shopapp/product_details.html"
    # model = Product
    queryset = Product.objects.prefetch_related("images")
    context_object_name = "product"


class ProductsListView(ListView):
    template_name = "shopapp/products_list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "shopapp.add_product"
    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        return response


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name_suffix = "_update_form"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        if (
            self.request.user == self.get_object().created_by
            and self.request.user.has_perm("shopapp.change_product")
        ):
            return True

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist("images"):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrdersListView(LoginRequiredMixin, ListView):
    queryset = Order.objects.select_related("user").prefetch_related(
        "products"
    )


class OrderDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"

    queryset = Order.objects.select_related("user").prefetch_related(
        "products"
    )


class CreateOrderView(CreateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    success_url = reverse_lazy("shopapp:orders_list")

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["products"].queryset = Product.objects.filter(
            archived=False
        )
        return form


class UpdateOrderView(UpdateView):
    model = Order
    fields = "delivery_address", "promocode", "user", "products"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:order_details",
            kwargs={"pk": self.object.pk},
        )

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["products"].queryset = Product.objects.filter(
            archived=False
        )
        return form


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class OrdersExportView(PermissionRequiredMixin, View):

    permission_required = "shopapp.is_staff"

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by("pk").all()
        orders_data = [
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
        return JsonResponse({"orders": orders_data})


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        cache_key = "products_data_export"
        products_data = cache.get(cache_key)
        if products_data is None:
            products = Product.objects.order_by("pk").all()
            products_data = [
                {
                    "pk": product.pk,
                    "name": product.name,
                    "price": product.price,
                    "archived": product.archived,
                }
                for product in products
            ]
            cache.set(cache_key, products_data, 5)
        return JsonResponse({"products": products_data})


class UserOrdersListView(ListView):

    template_name = "shopapp/order_list.html"
    success_url = reverse_lazy("shopapp:order_list")

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        self.owner = get_object_or_404(User, id=user_id)
        queryset = (
            Order.objects.select_related("user")
            .prefetch_related("products")
            .filter(user_id=user_id)
        )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["owner"] = self.owner
        return context


class UserOrderDataExportView(View):

    def get(self, request: HttpRequest, **kwargs) -> JsonResponse:
        user_id = self.kwargs["user_id"]
        self.owner = get_object_or_404(User, id=user_id)
        cache_key = f"orders_data_export_for_{user_id}"
        orders_data = cache.get(cache_key)
        if orders_data is None:
            orders = Order.objects.filter(user_id=user_id).order_by("pk")
            orders_data = OrderSerializer(orders, many=True)
            cache.set(cache_key, orders_data, 300)
        return JsonResponse(orders_data.data, safe=False)

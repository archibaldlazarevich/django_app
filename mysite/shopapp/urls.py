from django.urls import path, include
# from django.views.decorators.cache import cache_page

from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndexView,
    GroupsListView,
    ProductDetailsView,
    ProductsListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrdersListView,
    OrderDetailsView,
    CreateOrderView,
    UpdateOrderView,
    OrderDeleteView,
    OrdersExportView,
    ProductsDataExportView,
    LatestProductsFeed,
    UserOrdersListView,
    UserOrderDataExportView,
)

from .api import ProductViewSet, OrderViewSet

app_name = "shopapp"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    # path("", cache_page(10)(ShopIndexView.as_view()), name="index"),# без декоратора в классе view
    path("", (ShopIndexView.as_view()), name="index"),
    path("api/", include(routers.urls)),
    path("groups/", GroupsListView.as_view(), name="groups_list"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/latest/feed/", LatestProductsFeed(), name="products-feed"),
    path(
        "products/export/",
        ProductsDataExportView.as_view(),
        name="products-export",
    ),
    path(
        "products/create/", ProductCreateView.as_view(), name="product_create"
    ),
    path(
        "products/<int:pk>/",
        ProductDetailsView.as_view(),
        name="product_details",
    ),
    path(
        "products/<int:pk>/update/",
        ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "products/<int:pk>/archive/",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/create/", CreateOrderView.as_view(), name="order_create"),
    path("orders/export/", OrdersExportView.as_view(), name="orders_export"),
    path("orders/<int:pk>/", OrderDetailsView.as_view(), name="order_details"),
    path(
        "orders/<int:pk>/update/",
        UpdateOrderView.as_view(),
        name="order_update",
    ),
    path(
        "orders/<int:pk>/delete/",
        OrderDeleteView.as_view(),
        name="order_delete",
    ),
    path(
        "users/<int:user_id>/orders/",
        UserOrdersListView.as_view(),
        name="orders_list_view",
    ),
    path(
        "users/<int:user_id>/orders/export/",
        UserOrderDataExportView.as_view(),
        name="user_order_list_export",
    ),
]

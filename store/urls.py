
from django.urls import path
from .views import (
    LatestProductList,
    OrderItemView,
    ProductDetailView,
    CategoryListView,
    OrdersListView,
    AddItemToCartView,
    RemoveFromCartView,
    RandomProduct
)
urlpatterns = [
    path('products/', LatestProductList.as_view(), name="products_list"),
    path('product/<int:id>/',
         ProductDetailView.as_view(), name="product_detail"),
    path('products/categories/', CategoryListView.as_view(), name="categories"),
    path('orders/', OrdersListView.as_view(), name="orders"),
    path('my/orders/', OrderItemView.as_view(), name="order_items"),
    path('add/cart/product/',
         AddItemToCartView.as_view(), name="add_cart"),
    path('remove/cart/',
         RemoveFromCartView.as_view(), name="remove_cart"),
    path('random/product/', RandomProduct.as_view(), name="random_product")
]

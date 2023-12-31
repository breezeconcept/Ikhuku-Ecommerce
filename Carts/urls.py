from django.urls import path
from .views import CartItemListView, CartItemDetailView, CartItemRemoveView

urlpatterns = [
    path('cart/', CartItemListView.as_view(), name='cart-list'),
    path('cart/<uuid:id>/', CartItemDetailView.as_view(), name='cart-detail'),
    # URL pattern for removing a product from the cart
    path('cart/remove/<uuid:product_id>/', CartItemRemoveView.as_view(), name='cart-remove'),
]

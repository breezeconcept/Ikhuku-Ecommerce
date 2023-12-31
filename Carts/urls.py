from django.urls import path
from .views import CartItemListView, CartItemDetailView, CartItemRemoveView, CartItemUpdateView, CartItemCreateView

urlpatterns = [
    path('cart/list/', CartItemListView.as_view(), name='cart-list'),
    path('cart/add/', CartItemCreateView.as_view(), name='cart-create'),
    path('cart/get/<uuid:product_id>/', CartItemDetailView.as_view(), name='cart-detail'),
    path('cart/remove/<uuid:product_id>/', CartItemRemoveView.as_view(), name='cart-remove'),
    path('cart/update/<uuid:product_id>/', CartItemUpdateView.as_view(), name='cart-update'),
]

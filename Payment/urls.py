from django.urls import path
from .views import OrderListView, OrderDetailView, CheckoutInitiationView, PaymentProcessingView
urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('checkout/', CheckoutInitiationView.as_view(), name='checkout-initiation'),
    path('process-payment/', PaymentProcessingView.as_view(), name='payment-processing'),
    # Add other URLs as needed for specific order-related functionalities
]

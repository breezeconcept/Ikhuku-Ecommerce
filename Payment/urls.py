from django.urls import path
from .views import OrderListView, OrderDetailView, CheckoutInitiationView, OrderUpdateView, PaystackInitiationView, PaystackPaymentCallbackView, PaystackWebhookView
urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('checkout/', CheckoutInitiationView.as_view(), name='checkout-initiation'),
    path('update-order/', OrderUpdateView.as_view(), name='update-order'),

    # path('process-payment/', PaymentProcessingView.as_view(), name='payment-processing'),
    path('initiate-payment/', PaystackInitiationView.as_view(), name='initiate-payment'),
    path('paystack-callback/', PaystackPaymentCallbackView.as_view(), name='paystack-callback'),
    path('paystack-webhook/', PaystackWebhookView.as_view(), name='paystack-webhook'),
]


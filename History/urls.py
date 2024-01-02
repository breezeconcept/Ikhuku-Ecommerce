from django.urls import path
from .views import OrderHistoryView, DetailedOrderHistoryView

urlpatterns = [
    # path('order-history/', OrderHistoryView.as_view(), name='order-history'),
    # path('transaction-history/', TransactionHistoryView.as_view(), name='transaction-history'),
    path('history/', OrderHistoryView.as_view(), name='order-history'),
    path('history_details/<uuid:id>/', DetailedOrderHistoryView.as_view(), name='detailed-order-history'),
    # other URLs...
]

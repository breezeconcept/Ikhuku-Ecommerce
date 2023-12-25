from django.urls import path
from .views import OrderHistoryView, TransactionHistoryView

urlpatterns = [
    path('order-history/', OrderHistoryView.as_view(), name='order-history'),
    path('transaction-history/', TransactionHistoryView.as_view(), name='transaction-history'),
    # other URLs...
]

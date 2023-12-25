from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from Payment.models import Order
from Payment.serializers import OrderSerializer
from .models import Transaction
from .serializers import TransactionSerializer  # Import your Transaction serializer



class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)




class TransactionHistoryView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(order__user=user)

# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from Payment.models import Order
# from Payment.serializers import OrderSerializer
# from .models import Transaction
# from .serializers import TransactionSerializer  # Import your Transaction serializer



# class OrderHistoryView(generics.ListAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Order.objects.filter(user=user)




# class TransactionHistoryView(generics.ListAPIView):
#     serializer_class = TransactionSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Transaction.objects.filter(order__user=user)



from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from Payment.models import Order
from .serializers import OrderHistorySerializer
from .serializers import DetailedOrderHistorySerializer
from django.db.models import Prefetch
from Products.models import Product



class OrderHistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderHistorySerializer

    def get_queryset(self):
        user = self.request.user

        # Prefetch related products to avoid N+1 query problem
        return Order.objects.filter(user=user).prefetch_related(
            Prefetch('products', queryset=Product.objects.all())
        )



class DetailedOrderHistoryView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DetailedOrderHistorySerializer
    queryset = Order.objects.all()
    lookup_field = 'id'  # Assuming the URL parameter is the order ID
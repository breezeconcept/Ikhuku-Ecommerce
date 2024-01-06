# from rest_framework import serializers
# from .models import Transaction

# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = '__all__'  # Include all fields or specify the required fields



from rest_framework import serializers
from Payment.models import Order
from Products.serializers import ProductSerializer

class OrderHistorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)  # Serialize associated products
    class Meta:
        model = Order
        fields = ['id', 'status', 'total_amount', 'products', 'completed_at']


class DetailedOrderHistorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)  # Serialize associated products

    class Meta:
        model = Order
        fields = ['id', 'status', 'total_amount', 'products', 'receipt']


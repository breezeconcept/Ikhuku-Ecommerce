from rest_framework import serializers
from .models import Order
from Products.serializers import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)  # Serialize associated products
    class Meta:
        model = Order
        fields = '__all__'  # Add more fields as necessary

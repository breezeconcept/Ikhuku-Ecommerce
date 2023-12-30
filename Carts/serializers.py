from rest_framework import serializers
from .models import CartItem
from Products.serializers import ProductSerializer  # Import your Product serializer here

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Assuming you have a ProductSerializer for the Product model
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'user']

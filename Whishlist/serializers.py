from rest_framework import serializers
from .models import Favorite
from Products.serializers import ProductSerializer  # Import your Product serializer here

class FavoriteSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Favorite
        fields = '__all__'




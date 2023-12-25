# serializers.py
from rest_framework import serializers
from .models import Product, Category
from django_filters import rest_framework as filters

class ProductFilter(filters.FilterSet):
    # Define filters for search functionality
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name', 'description']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'







class MerchantProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class MerchantProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class MerchantProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class MerchantProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class MerchantProductDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
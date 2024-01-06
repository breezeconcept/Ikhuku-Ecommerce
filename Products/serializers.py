# serializers.py
from rest_framework import serializers
from .models import Product, Category, SubCategory
from django_filters import rest_framework as filters

class ProductFilter(filters.FilterSet):
    # Define filters for search functionality
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name', 'description']


class ProductSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'     


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category']

class SubCategorySerializer2(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category']




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'







class MerchantProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# class MerchantProductDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'

class MerchantProductCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    seller = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())
    image = serializers.ImageField()

    class Meta:
        model = Product
        fields = '__all__'

class MerchantProductUpdateDestroySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    seller = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())
    image = serializers.ImageField()

    class Meta:
        model = Product
        fields = '__all__'

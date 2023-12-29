# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Product, Category
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from Accounts.permissions import IsMerchant
from Accounts.models import SellerProfile
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import (
    ProductFilter,

     CategorySerializer,
     ProductSerializer, 

     MerchantProductListSerializer, 
     MerchantProductDetailSerializer,
     MerchantProductCreateSerializer,
     MerchantProductUpdateSerializer,
    #  MerchantProductDeleteSerializer
     )





############  This is for pagination

# class ProductPageView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     pagination_class = PageNumberPagination

#     def get(self, request, *args, **kwargs):
#         self.queryset = Product.objects.all()  # You can adjust this queryset based on your needs
#         return self.list(request, *args, **kwargs)




################  This is for search functinality (it's also paginated)
###########  This endpoint can be accessed by anybody

class ProductsSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter    
    pagination_class = PageNumberPagination






######## To get a list of all the categories
###########  This endpoint can be accessed by anybody

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer





######### To get all products in a single category (it's also paginated)
###########  This endpoint can be accessed by anybody

class ProductByCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination


    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Product.objects.filter(category_id=category_id)
    


#########   To create category
###########  This endpoint can only be accessed by admin

class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]





#########   To update category
###########  This endpoint can only be accessed by admin

class CategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'  # Use 'id' or any other field to identify the category





#########   To delete category
###########  This endpoint can only be accessed by admin

class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'  # Use 'id' or any other field to identify the category





######### TO VIEW ALL PRODUCTS
##########   Endpoint can be accessed by anybody

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    




##########  TO VIEW SINGLE PRODUCT DETAILS
##########   Endpoint can be accessed by anybody

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'  # Specify the field to use for retrieving the product (e.g., 'id' or 'slug')







###################################  FOR SELLERS

##########  TO VIEW ALL PRODUCTS 
##########   Endpoint can only be accessed by sellers (ONLY THE PRODUCTS CREATED BY THEM)

class MerchantProductListView(generics.ListAPIView):
    serializer_class = MerchantProductListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination


    def get_queryset(self):
        merchant = self.request.user  # Replace this with your logic to retrieve the merchant
        return Product.objects.filter(merchant=merchant)





##########  TO VIEW SINGLE PRODUCT DETAILS 
##########   Endpoint can only be accessed by sellers (ONLY THE PRODUCTS CREATED BY THEM)

class MerchantProductDetailView(generics.RetrieveAPIView):
    serializer_class = MerchantProductDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'  # Replace with the identifier used in your Product model

    def get_queryset(self):
        merchant = self.request.user  # Replace this with your logic to retrieve the merchant
        return Product.objects.filter(merchant=merchant)





##########  TO CREATE A PRODUCT
##########   Endpoint can only be accessed by sellers 

# class MerchantProductCreateView(generics.CreateAPIView):
#     serializer_class = MerchantProductCreateSerializer
#     permission_classes = [IsMerchant]  # Only authenticated merchants can create products

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)  # Assign the logged-in user as the merchant


##########  TO CREATE A PRODUCT
##########   Endpoint can only be accessed by sellers
# class MerchantProductCreateView(generics.CreateAPIView):
#     serializer_class = MerchantProductCreateSerializer
#     permission_classes = [IsMerchant]


#     def post(self, request, *args, **kwargs):
#         user = self.request.user
#         seller = SellerProfile.objects.get(user=user)

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(user=user, seller=seller)


# class MerchantProductCreateView(generics.CreateAPIView):
#     serializer_class = MerchantProductCreateSerializer
#     permission_classes = [IsMerchant]

#     def perform_create(self, serializer):
#         user=self.request.user
#         seller=self.request.user.sellerprofile
#         serializer.save(user=user, seller=seller)

class MerchantProductCreateView(generics.CreateAPIView):
    serializer_class = MerchantProductCreateSerializer
    permission_classes = [IsMerchant]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        seller=self.request.user.sellerprofile
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, seller=seller)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


        

##########  TO UPDATE A PRODUCT
##########   Endpoint can only be accessed by sellers (ONLY THE PRODUCTS CREATED BY THEM)

class MerchantProductUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = MerchantProductUpdateSerializer
    lookup_field = 'id'  # Replace with the identifier used in your Product model
    permission_classes = [IsMerchant]  # Only authenticated merchants can update/delete products

    # def get_queryset(self):
    #     merchant = self.request.user  # Replace this with your logic to retrieve the merchant
    #     return Product.objects.filter(merchant=merchant)





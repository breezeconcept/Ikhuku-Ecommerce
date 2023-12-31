# views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import Product, Category
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from Accounts.permissions import IsMerchant
from Accounts.models import SellerProfile
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from Whishlist.models import Favorite
from rest_framework.views import APIView

from .serializers import (
    ProductFilter,

     CategorySerializer,
     ProductSerializer, 

     MerchantProductListSerializer, 
    #  MerchantProductDetailSerializer,
     MerchantProductCreateSerializer,
     MerchantProductUpdateDestroySerializer,
    #  MerchantProductDeleteSerializer,
    ProductSearchSerializer
     )




class ProductFilterView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


        
        

    def get_queryset(self):
        queryset = Product.objects.all()

        # Filter by search query
        search_query = self.request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        # Filter by category
        # category = self.request.query_params.get('category')
        # if category:
        #     queryset = queryset.filter(category=category)
        category_name = self.request.query_params.get('category')
        if category_name:
            # Filter products by category name
            queryset = queryset.filter(category__name__iexact=category_name)

        # Filter by unique price upwards
        unique_price_up = self.request.query_params.get('unique_price_up')
        if unique_price_up:
            queryset = queryset.filter(price__gte=unique_price_up)

        # Filter by unique price downwards
        unique_price_down = self.request.query_params.get('unique_price_down')
        if unique_price_down:
            queryset = queryset.filter(price__lte=unique_price_down)


        # Filter by price range (min_price and max_price)
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price and max_price:
            queryset = queryset.filter(price__range=(min_price, max_price))

        return queryset.distinct()




############  This is for pagination

# class ProductPageView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     pagination_class = PageNumberPagination

#     def get(self, request, *args, **kwargs):
#         self.queryset = Product.objects.all()  # You can adjust this queryset based on your needs
#         return self.list(request, *args, **kwargs)




################  This is for search functionality (it's also paginated)
###########  This endpoint can be accessed by anybody

class ProductsSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter    
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]






######## To get a list of all the categories
###########  This endpoint can be accessed by anybody

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]



######### To get all products in a single category (it's also paginated)
###########  This endpoint can be accessed by anybody

class ProductByCategoryView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Product.objects.filter(category_id=category_id)
    

class ProductBySearchView(generics.ListAPIView):
    serializer_class = ProductSearchSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


    def get_queryset(self):
        search_query = self.request.query_params.get('search')
        if search_query:
            # Assuming 'name' or any field in Product model to be searched
            queryset = Product.objects.filter(name__icontains=search_query)
            return queryset
        else:
            # Return all products if no search query is provided
            return Product.objects.all()
    




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






######## TO VIEW ALL PRODUCTS   ############
##########   Endpoint can be accessed by anybody

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


##########  TO VIEW SINGLE PRODUCT DETAILS
##########   Endpoint can be accessed by anybody

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'  
    permission_classes = [AllowAny]






###################################  FOR SELLERS   ####################################################

##########  TO VIEW ALL PRODUCTS 
##########   Endpoint can only be accessed by sellers (ONLY THE PRODUCTS CREATED BY THEM)

class MerchantProductListView(generics.ListAPIView):
    serializer_class = MerchantProductListSerializer
    permission_classes = [IsMerchant]
    pagination_class = PageNumberPagination

    # def get_queryset(self):
    #     seller_id = self.request.user.sellerprofile
    #     return Product.objects.filter(seller_id=seller_id)
    
    def get_queryset(self):
        # Retrieve the SellerProfile instance related to the authenticated user
        seller_profile = get_object_or_404(SellerProfile, user=self.request.user)

        # Retrieve the ID of the SellerProfile to filter products
        seller_id = seller_profile.id

        return Product.objects.filter(seller_id=seller_id)
    


##########  TO VIEW SINGLE PRODUCT DETAILS 
##########   Endpoint can only be accessed by sellers (ONLY THE PRODUCTS CREATED BY THEM)

# class MerchantProductDetailView(generics.RetrieveAPIView):
#     serializer_class = MerchantProductDetailSerializer
#     permission_classes = [IsAuthenticated]
#     lookup_field = 'id'  

#     def get_queryset(self):
#         seller_id = self.request.user.sellerprofile 
#         return Product.objects.filter(seller_id=seller_id)



##########  TO CREATE A PRODUCT
##########   Endpoint can only be accessed by sellers

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
    serializer_class = MerchantProductUpdateDestroySerializer
    permission_classes = [IsMerchant] 
    lookup_field = 'id' 
    

    def get_queryset(self):
        # Retrieve the SellerProfile instance related to the authenticated user
        seller_profile = get_object_or_404(SellerProfile, user=self.request.user)

        # Retrieve all products associated with the authenticated seller
        return Product.objects.filter(seller=seller_profile)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.kwargs['id'])
        self.check_object_permissions(self.request, obj)
        return obj






class CheckProductFavouriteView(APIView):
    def get(self, request, product_id):
        user = request.user
        product = get_object_or_404(Product, id=product_id)
        
        # Check if the product exists in the user's favorites
        is_favourite = Favorite.objects.filter(user=user, product=product).exists()

        # Return response indicating if the product is a favorite or not
        return Response({'is_favourite': is_favourite}, status=status.HTTP_200_OK)


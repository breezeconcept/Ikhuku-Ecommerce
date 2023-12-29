from django.urls import path
from .views import (
    ProductsSearchView,

    CategoryListView,
    ProductByCategoryView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,

    ProductListView, 
    ProductDetailView, 

    MerchantProductListView, 
    MerchantProductDetailView, 
    MerchantProductCreateView,
    MerchantProductUpdateDestroyView,
    # MerchantProductDeleteView
    )


urlpatterns = [
    ############    For search 
    path('products/search/', ProductsSearchView.as_view(), name='product-search'),

    #############   Get all categories
    path('categories/', CategoryListView.as_view(), name='category-list'),

    #############    Get products by category
    path('categories/<uuid:category_id>/products/', ProductByCategoryView.as_view(), name='products-by-category'),
    
    ##############    To create category (for admins)
    path('categories/create/', CategoryCreateView.as_view(), name='category-create'),

    path('categories/<uuid:id>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<uuid:id>/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    # FOR BUYERS
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<uuid:id>/', ProductDetailView.as_view(), name='product-detail'),

    # FOR SELLERS
    path('merchant/products/getAll/', MerchantProductListView.as_view(), name='merchant-product-list'),
    path('merchant/products/get/<uuid:id>/', MerchantProductDetailView.as_view(), name='merchant-product-detail'),
    path('merchant/products/create/', MerchantProductCreateView.as_view(), name='product-create'),
    path('merchant/products/<uuid:id>/', MerchantProductUpdateDestroyView.as_view(), name='product-update-delete'),
    # path('merchant/products/<uuid:id>/', MerchantProductDeleteView.as_view(), name='product-update-delete'),

]

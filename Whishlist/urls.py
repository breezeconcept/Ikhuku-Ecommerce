from django.urls import path
from .views import FavoriteCreateView, FavoriteDeleteView, FavoriteListView, FavoriteRemoveView

urlpatterns = [
    path('favorites/add/', FavoriteCreateView.as_view(), name='favorite-add'),
    path('favorites/<uuid:id>/', FavoriteDeleteView.as_view(), name='favorite-remove'),
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
    
    # URL pattern for removing a product from the wishlist
    path('favorites/remove/<uuid:product_id>/', FavoriteRemoveView.as_view(), name='favorite-remove'),
]

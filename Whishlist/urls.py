from django.urls import path
from .views import FavoriteCreateView, FavoriteListView, FavoriteRemoveView, FavoriteItemDetailView

urlpatterns = [
    path('favorites/add/', FavoriteCreateView.as_view(), name='favorite-add'),
    # path('favorites/<uuid:id>/', FavoriteDeleteView.as_view(), name='favorite-remove'),
    path('favorites/list/', FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/remove/<uuid:product_id>/', FavoriteRemoveView.as_view(), name='favorite-remove'),
    path('favorites/get/<uuid:product_id>/', FavoriteItemDetailView.as_view(), name='favorite-get'),
]

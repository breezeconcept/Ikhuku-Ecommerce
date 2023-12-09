from django.urls import path
from .views import FavoriteCreateView, FavoriteDeleteView, FavoriteListView

urlpatterns = [
    path('favorites/add/', FavoriteCreateView.as_view(), name='favorite-add'),
    path('favorites/remove/<uuid:id>/', FavoriteDeleteView.as_view(), name='favorite-remove'),
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
]

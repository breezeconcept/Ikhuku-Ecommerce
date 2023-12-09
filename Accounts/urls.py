from django.urls import path
from .views import CreateUserView, UpdateUserView, UserLoginView, UserLogoutView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='user-create'),
    path('update-account/<uuid:pk>/', UpdateUserView.as_view(), name='user-detail'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
]

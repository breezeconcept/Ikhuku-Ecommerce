from django.urls import path
from .views import (
    CreateUserView, 
    UpdateUserView, 
    UserLoginView, 
    # UserLogoutView, 
    EmailVerificationView, 
    PasswordResetRequestView, 
    PasswordResetConfirmView,
    ChangePasswordView,
    SellerProfileCreateView,
    SellerVerificationView,
    GrantAdminRightsView,
    RevokeAdminRightsView,
    GrantStaffRightsView,
    RevokeStaffRightsView,
    # TokenRefreshView,
    # TokenVerifyView,
    # SellerProfileListView,
    SellerProfileRetrieveUpdateView,
    # SellerProfileRetrieveDestroyView,
    )
from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='user-create'),
    path('account/verify/<uuid:id>/', EmailVerificationView.as_view(), name='account_verify'),
    path('update-account/', UpdateUserView.as_view(), name='user-detail'),

    path('login/', UserLoginView.as_view(), name='user-login'),
    # path('token/create/', TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # path('logout/', UserLogoutView.as_view(), name='user-logout'),

    path('password/reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password/reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/change/', ChangePasswordView.as_view(), name='change-password'),

    path('create-seller-profile/', SellerProfileCreateView.as_view(), name='create-seller-profile'),
    path('seller-profile-verify/<uuid:id>/', SellerVerificationView.as_view(), name='verify-seller'),
    # path('seller-profile/', SellerProfileListView.as_view(), name='create-seller-profile'),
    path('seller-profile/', SellerProfileRetrieveUpdateView.as_view(), name='seller-profile'),
    # path('seller-profile-delete/', SellerProfileRetrieveDestroyView.as_view(), name='create-seller-profile'),

    path('admin-rights-grant/<uuid:id>/', GrantAdminRightsView.as_view(), name='grant-admin-rights'),
    path('admin-rights-revoke/<uuid:id>/', RevokeAdminRightsView.as_view(), name='revoke-admin-rights'),

    path('staff-rights-grant/<uuid:id>/', GrantStaffRightsView.as_view(), name='grant-admin-rights'),
    path('staff-rights-revoke/<uuid:id>/', RevokeStaffRightsView.as_view(), name='revoke-admin-rights'),
]



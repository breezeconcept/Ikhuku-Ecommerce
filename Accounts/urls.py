from django.urls import path
from .views import (
    CreateUserView, 
    UpdateUserView, 
    UserLoginView, 
    UserLogoutView, 
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
    TokenRefreshView,
    TokenVerifyView,
    )
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView,
# )

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='user-create'),
    path('confirm-email/<uuid:id>/', EmailVerificationView.as_view(), name='confirm-email'),

    path('update-account/<uuid:pk>/', UpdateUserView.as_view(), name='user-detail'),

    path('login/', UserLoginView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # path('logout/', UserLogoutView.as_view(), name='user-logout'),

    path('password/reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password/reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('create-seller-profile/', SellerProfileCreateView.as_view(), name='create-seller-profile'),
    path('verify-seller/<int:pk>/', SellerVerificationView.as_view(), name='verify-seller'),
    path('grant-admin-rights/<int:pk>/', GrantAdminRightsView.as_view(), name='grant-admin-rights'),
    path('revoke-admin-rights/<int:pk>/', RevokeAdminRightsView.as_view(), name='revoke-admin-rights'),
    path('grant-staff-rights/<int:pk>/', GrantStaffRightsView.as_view(), name='grant-admin-rights'),
    path('revoke-staff-rights/<int:pk>/', RevokeStaffRightsView.as_view(), name='revoke-admin-rights'),
]



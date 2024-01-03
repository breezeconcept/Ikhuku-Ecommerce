"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Accounts.views import EmailVerificationView, PasswordResetConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include("Accounts.urls")),
    path('api/user/', include("Products.urls")),
    path('api/user/', include("Carts.urls")),
    path('api/user/', include("Payment.urls")),
    path('api/user/', include("History.urls")),
    path('api/user/', include("Whishlist.urls")),
    path('api/', include('ecommerce.swagger')),
    path('account/verify/<uuid:id>/', EmailVerificationView.as_view(), name='account_verify'),
    path('password/reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
# Add the following line at the end to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
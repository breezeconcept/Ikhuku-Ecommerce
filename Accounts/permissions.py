from rest_framework import permissions
from rest_framework.permissions import BasePermission



class IsMerchant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_merchant
    

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

# permission_classes = [IsMerchant]

class IsSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only permissions for non-authenticated users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Check if the user is a superuser
        return request.user and request.user.is_superuser


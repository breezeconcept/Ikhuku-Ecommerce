from django.contrib import admin
from .models import CartItem
from django.contrib.auth.admin import UserAdmin


# class CustomUserAdmin(UserAdmin):
#     readonly_fields = ('id',)

# admin.site.register(CartItem, CustomUserAdmin)
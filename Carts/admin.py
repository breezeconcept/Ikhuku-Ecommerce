from django.contrib import admin
from .models import CartItem



class CartItemAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)  # Define readonly fields if needed
    list_display = ('id', 'product', 'quantity', 'user')  # Display fields in the list view

admin.site.register(CartItem, CartItemAdmin)
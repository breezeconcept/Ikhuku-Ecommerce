from django.contrib import admin
from .models import Product, Category, SubCategory



class SubCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)  # Define readonly fields if needed
    # list_display = ('id', 'product', 'quantity', 'user')  # Display fields in the list view

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)  # Define readonly fields if needed
    # list_display = ('id', 'product', 'quantity', 'user')  # Display fields in the list view



# Register your models here.
admin.site.register(Product)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
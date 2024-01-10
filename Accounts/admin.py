from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser, SellerProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number')

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'address')}),
        ('Permissions', {
            'fields': ('id', 'is_active', 'is_verified', 'is_merchant', 'is_admin', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_verified', 'date_joined', 'last_login')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    readonly_fields = ('id',)

admin.site.register(CustomUser, CustomUserAdmin)

class CartItemAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)  # Define readonly fields if needed
    list_display = ('id', 'user', 'company_name', 'profile_picture', 'business_license', 'is_verified')  # Display fields in the list view

admin.site.register(SellerProfile, CartItemAdmin)

# admin.site.register(CustomUser)

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, profile_picture, address, password=None, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_verified', False)
        extra_fields.setdefault('is_merchant', False)
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, phone_number=phone_number, profile_picture=profile_picture, address=address, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    
    def create_superuser(self, email, first_name, last_name, phone_number, password=None, profile_picture=None, address=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('is_merchant', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser needs to be staff. Do not set is_staff.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser needs to be superuser. Do not set is_superuser.')

        return self.create_user(email, first_name, last_name, phone_number, profile_picture, address, password, **extra_fields)




class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_merchant = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)


    class Meta:
        db_table = 'CustomUser'

    objects = CustomUserManager()  # Set the custom user manager

    # Set email as the primary identifier for authentication
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return f"{self.email}"
    
    def has_module_perms(self, app_label):
        return True  # Assuming all users have permission to access all apps/modules




class SellerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_profile')
    company_name = models.CharField(max_length=100)
    business_license = models.FileField(upload_to='business_licenses/')
    is_verified = models.BooleanField(default=False)
    # Add other fields related to the seller profile


    def __str__(self):
        return f"Seller Profile for {self.user.email}"



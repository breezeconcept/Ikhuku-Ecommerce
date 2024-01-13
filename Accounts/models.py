from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, address, password=None, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_verified', False)
        extra_fields.setdefault('is_merchant', False)
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, phone_number=phone_number, address=address, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    
    def create_superuser(self, email, first_name, last_name, phone_number, password=None, address=None, **extra_fields):
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

        return self.create_user(email, first_name, last_name, phone_number, address, password, **extra_fields)




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
    STATUS_CHOICES = [
        ('sole proprietorship', 'Sole Proprietorship'),
        ('limited liability company', 'Limited Liability Company'),
        ('corporation', 'Corporation'),
        ('partnership', 'Partnership'),
        ('professional corporation', 'Professional Corporation'),
        ('cooperative', 'Cooperative'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=100)
    business_reg_no = models.CharField(max_length=100, blank=True, null=True)
    business_cert = models.FileField(upload_to='business_cert/', blank=True, null=True)
    business_address = models.CharField(max_length=100, blank=True, null=True)
    business_address_proof = models.FileField(upload_to='business_address_proof/', blank=True, null=True)
    business_type = models.CharField(max_length=100, choices=STATUS_CHOICES, default="sole proprietorship", blank=True, null=True)

    is_seller_accept_terms = models.BooleanField(default=False)

    nin_number = models.CharField(max_length=100, null=True)
    nin_card = models.FileField(upload_to='nin_card/', blank=True, null=True)
    nin_selfie = models.FileField(upload_to='nin_selfie/', blank=True, null=True)

    account_name = models.CharField(max_length=100, null=True)
    bank_name = models.CharField(max_length=100, null=True)
    account_number = models.IntegerField(null=True)

    is_return_refund_accept = models.BooleanField(default=False, blank=True, null=True)
    is_warranty = models.BooleanField(default=False, blank=True, null=True)
    warranty_duration = models.IntegerField(blank=True, null=True)

    business_logo = models.ImageField(upload_to='business_logo/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True)
    personal_address = models.CharField(max_length=100, blank=True, null=True)
    personal_address_proof = models.FileField(upload_to='personal_address_proof/', blank=True, null=True)
    business_bio = models.TextField(max_length=255, null=True)

    is_platform_policy_accept = models.BooleanField(default=False)
    is_use_verify_info = models.BooleanField(default=False)

    business_license = models.FileField(upload_to='business_licenses/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    # Add other fields related to the seller profile


    def __str__(self):
        return f"Seller Profile for {self.user.email}"



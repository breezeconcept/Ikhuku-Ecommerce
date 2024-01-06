
# models.py
from django.db import models
import uuid
from django.conf import settings
from Accounts.models import SellerProfile



class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    # Other fields...


    def __str__(self):
        return self.name
    


class SubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Other fields...


    def __str__(self):
        return self.name
    



# def get_default_subcategory():
#     return SubCategory.objects.get_or_create(name='Unknown')[0]


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products', null=True, default=get_default_subcategory)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products', null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    # Other fields...


    def __str__(self):
        return self.name

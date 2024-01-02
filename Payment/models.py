from django.db import models
from django.conf import settings
import uuid
from Products.models import Product
    
 

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    reference = models.CharField(max_length=100, blank=True, null=True)  # Your system's reference
    paystack_reference = models.CharField(max_length=100, blank=True, null=True)  # Paystack's reference
    completed_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    receipt = models.FileField(upload_to='order_receipt/', blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='orders')  # Assuming ManyToMany relationship with Product


    # Other fields as needed for your order model

    def __str__(self):
        return f"Order #{self.id} - Total: {self.total_amount}"

from django.db import models
from django.conf import settings
from Products.models import Product  # Replace 'your_app' with your app name
import uuid

class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"User: {self.user.email} - Product: {self.product.name} - Quantity: {self.quantity} "



# {
#   "status": 500,
#   "success": false,
#   "data": [],
#   "error": "connection to server at \"104.248.143.148\", port 5432 failed: Connection refused\n\tIs the server running on that host and accepting TCP/IP connections?\n"
# }
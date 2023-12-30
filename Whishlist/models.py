from django.db import models
from django.conf import settings
from Products.models import Product  # Replace 'Products' with your app name
import uuid

class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_favourite = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"User: {self.user.email} - Favorite Product: {self.product.name}"

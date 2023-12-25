from django.db import models
from django.conf import settings
import uuid

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    # Add more fields as needed, such as status, shipping details, etc.

    def __str__(self):
        return f"Order #{self.id} - Total: {self.total_amount}"

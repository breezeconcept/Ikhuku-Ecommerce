# from django.db import models
# from Payment.models import Order  # Update with the correct import for your Order model
# import uuid

# class Transaction(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     payment_id = models.CharField(max_length=100)
#     status = models.CharField(max_length=50)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     # Add other fields as needed to store transaction details
#     # ...

#     # You can add methods or fields specific to transaction history
#     def __str__(self):
#         return f"Order #{self.order.id} - Payment: {self.payment_id}"

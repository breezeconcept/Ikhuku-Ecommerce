from django.core.management.base import BaseCommand
from Products.models import Product

class Command(BaseCommand):
    help = 'Clears the Product table'

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()

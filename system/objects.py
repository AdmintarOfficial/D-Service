# Library Global
from psycopg2.extras import DateTimeTZRange
from datetime import timedelta
from django.utils import timezone

# Library Models
from django.db.models import Sum

# Library App
from . import models, functions

# Products
def store(request, value):
    if value is not None:
        # Products
        product = models.Products.objects.all()
        items = models.Itemlist.objects.filter(item_status=1).order_by('pk')
        
        if value == 'Product':
            return product
        elif value == 'Items':
            return items
        else:
            return None
    else:
        store = models.Itemlist.objects.filter(item_status=1).order_by('pk')
        return store

# Items Cart
def Cart(request):
    items = models.SellProduct.objects.all()
    return items
    
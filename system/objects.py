# Library Global
from psycopg2.extras import DateTimeTZRange
from datetime import timedelta
from django.utils import timezone

# Library Models
from django.db.models import Sum

# Library App
from . import models, functions
from log import models as models_log

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

# Cart Check
def Cart(request, value, barcode):
    cart_chk = models.SellProduct.objects.filter(barcode=barcode)
    cart_list = models.SellProduct.objects.filter(username=request.user.username)
    total_price = models.SellProduct.objects.filter(username=request.user.username).aggregate(Sum('price'))['price__sum']
    total_count = models.SellProduct.objects.filter(username=request.user.username).aggregate(Sum('count'))['count__sum']
    
    if value == 'Check':
        return cart_chk
    elif value == 'List':
        return cart_list
    elif value == 'Total_Price':
        return total_price
    elif value == 'Total_Count':
        return total_count
    
# Billing Log
def Billing_Log(request, value, sell_id):
    billing_log = models_log.Selling_Log.objects.get(sell_id=sell_id)
    billing_detail_log = models_log.Sell_Detail_Log.objects.filter(sell_id=sell_id)
    billing_total_price_log = models_log.Sell_Detail_Log.objects.filter(sell_id=sell_id).aggregate(Sum('sell_price'))['sell_price__sum']
    
    change = int(billing_log.cash_money)+int(billing_log.transfer_money)-int(billing_log.total_price)
    
    if value == 'Billing_Log':
        return billing_log
    elif value == 'Billing_Detail_Log':
        return billing_detail_log
    elif value == 'Billing_Total_Price_Log':
        return billing_total_price_log
    elif value == 'Billing_Change_Log':
        return change
    
# Billing Log
def BillingTopup_Log(request, value, topup_id):
    billing_log = models_log.Topup_Log.objects.get(topup_id=topup_id)
    billing_detail_log = models_log.Topup_Detail_Log.objects.filter(topup_id=topup_id)
    billing_total_price_log = models_log.Topup_Detail_Log.objects.filter(topup_id=topup_id).aggregate(Sum('price'))['price__sum']
    
    change = int(billing_log.cash_money)+int(billing_log.transfer_money)-int(billing_log.total_price)
    
    if value == 'Billing_Log':
        return billing_log
    elif value == 'Billing_Detail_Log':
        return billing_detail_log
    elif value == 'Billing_Total_Price_Log':
        return billing_total_price_log
    elif value == 'Billing_Change_Log':
        return change
    
# Cart Topup Check
def Cart_Topup(request, value, barcode):
    cart_list = models.Topup.objects.filter(username=request.user.username)
    total_price = models.Topup.objects.filter(username=request.user.username).aggregate(Sum('price'))['price__sum']
    
    if value == 'List':
        return cart_list
    elif value == 'Total_Price':
        return total_price
    
    
# Members
def Members(request, name):
    members = models.Members.objects.all()
    member = models.Members.objects.filter(first_name=name)
    
    if name is not None:
        return member
    else:
        return members
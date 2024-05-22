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
    cart_chk = models.SellProduct.objects.filter(barcode_id=barcode)
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
    else:
        return None
    
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
    else:
        return None
    
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
    else:
        return None
    
# Cart Topup Check
def Cart_Topup(request, value, barcode):
    cart_list = models.Topup.objects.filter(username=request.user.username)
    total_price = models.Topup.objects.filter(username=request.user.username).aggregate(Sum('price'))['price__sum']
    
    if value == 'List':
        return cart_list
    elif value == 'Total_Price':
        return total_price
    else:
        return None
    
# Billing Cancel
def Bill_cancel(request, value):
    sell = models_log.Selling_Log.objects.filter(datetime__date=timezone.now().date())
    topup = models_log.Topup_Log.objects.filter(datetime__date=timezone.now().date())
    
    if value == 'Sell_Log':
        return sell
    elif value == 'Topup_Log':
        return topup
    else:
        return None
    
# Selling Report
def SellReport(request, value):
    sell_log = models_log.Selling_Log.objects.filter(active=True, datetime__date=timezone.now().date())
    topup_log = models_log.Topup_Log.objects.filter(active=True, datetime__date=timezone.now().date())
    
    # Cash
    sell_cash = models_log.Selling_Log.objects.filter(active=True, datetime__date=timezone.now().date()).aggregate(Sum('cash_money'))['cash_money__sum']
    topup_cash = models_log.Topup_Log.objects.filter(active=True, datetime__date=timezone.now().date()).aggregate(Sum('cash_money'))['cash_money__sum']
    # Transfer
    sell_transfer = models_log.Selling_Log.objects.filter(active=True, datetime__date=timezone.now().date()).aggregate(Sum('transfer_money'))['transfer_money__sum']
    topup_transfer = models_log.Topup_Log.objects.filter(active=True, datetime__date=timezone.now().date()).aggregate(Sum('transfer_money'))['transfer_money__sum']
    
    if sell_cash == None:
        sell_cash = 0
    
    if topup_cash == None:
        topup_cash = 0
        
    if sell_transfer == None:
        sell_transfer = 0
    
    if topup_transfer == None:
        topup_transfer = 0
    
    total_cash = int(sell_cash)+int(topup_cash)
    total_transfer = int(sell_transfer)+int(topup_transfer)
    total_price = int(total_cash)+int(total_transfer)
    
    if value == "Sell_Log":
        return sell_log
    elif value == "Topup_Log":
        return topup_log
    elif value == "Total_Cash":
        return total_cash
    elif value == "Total_Transfer":
        return total_transfer
    elif value == "Total_Price":
        return total_price
    else:
        return None
    
# Selling Report
def SellReport_Month(request, value):
    sell_log = models_log.Selling_Log.objects.filter(active=True, datetime__month=timezone.now().month)
    topup_log = models_log.Topup_Log.objects.filter(active=True, datetime__month=timezone.now().month)
    
    # Cash
    sell_cash = models_log.Selling_Log.objects.filter(active=True, datetime__month=timezone.now().month).aggregate(Sum('cash_money'))['cash_money__sum']
    topup_cash = models_log.Topup_Log.objects.filter(active=True, datetime__month=timezone.now().month).aggregate(Sum('cash_money'))['cash_money__sum']
    # Transfer
    sell_transfer = models_log.Selling_Log.objects.filter(active=True, datetime__month=timezone.now().month).aggregate(Sum('transfer_money'))['transfer_money__sum']
    topup_transfer = models_log.Topup_Log.objects.filter(active=True, datetime__month=timezone.now().month).aggregate(Sum('transfer_money'))['transfer_money__sum']
    
    if sell_cash == None:
        sell_cash = 0
    
    if topup_cash == None:
        topup_cash = 0
        
    if sell_transfer == None:
        sell_transfer = 0
    
    if topup_transfer == None:
        topup_transfer = 0
    
    total_cash = int(sell_cash)+int(topup_cash)
    total_transfer = int(sell_transfer)+int(topup_transfer)
    total_price = int(total_cash)+int(total_transfer)
    
    if value == "Sell_Log":
        return sell_log
    elif value == "Topup_Log":
        return topup_log
    elif value == "Total_Cash":
        return total_cash
    elif value == "Total_Transfer":
        return total_transfer
    elif value == "Total_Price":
        return total_price
    else:
        return None
    
# Stock Out
def StockOut(request, value, barcode):
    stock_out = models.StockOut.objects.all()
    cart_chk = models.StockOut.objects.filter(barcode_id=barcode)
    total_count = models.StockOut.objects.all().aggregate(Sum('count'))['count__sum']
    
    if value == 'Check':
        return cart_chk
    elif value == 'List':
        return stock_out
    elif value == 'Total_Count':
        return total_count
    else:
        return None
    
# Check Stock
def CheckStock(request, value):
    # Stock
    not_stock = models.CheckStock.objects.filter(active=False)
    check_stock = models.CheckStock.objects.filter(active=True)
    
    checking_price = check_stock.aggregate(Sum('price'))['price__sum']
    checking_count = check_stock.aggregate(Sum('count'))['count__sum']
    notcheck_price = not_stock.aggregate(Sum('price'))['price__sum']
    notcheck_count = not_stock.aggregate(Sum('count'))['count__sum']
    
    if value == "Checking_Price":
        return checking_price
    elif value == "Checking_Count":
        return checking_count
    elif value == "Notcheck_Price":
        return notcheck_price
    elif value == "Notcheck_Count":
        return notcheck_count
    elif value == True:
        return check_stock
    else:
        return not_stock
    
# Billing Report
def Bill_Report(request, value):
    sell = models_log.Selling_Log.objects.filter(datetime__month=timezone.now().month)
    topup = models_log.Topup_Log.objects.filter(datetime__month=timezone.now().month)
    
    if value == 'Sell_Log':
        return sell
    elif value == 'Topup_Log':
        return topup
    else:
        return None
    
# Members
def Members(request, name):
    members = models.Members.objects.all()
    
    if name is not None:
        member = models.Members.objects.filter(first_name__icontains=name)
        return member
    else:
        return members
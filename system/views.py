# Library Global
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Library App
from . import functions, contexts, objects

# Create your views here.

#== sale System ==#

# Index
def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', contexts.Context_Default(request))
    else:
        return redirect('/เข้าสู่ระบบ/')

# SamsungFinance
def samsungfinance(request):
    if request.user.is_authenticated:
        if 'tbarcode' in request.POST:
            # Add items to cart actions
            addcart = functions.AddCart(request)
            return HttpResponse(addcart, content_type="application/json")
        elif 'tdel_id' in request.POST:
            # Del item ID
            Del_id = functions.DelCart(request, 'Del_ID')
            return HttpResponse(Del_id, content_type="application/json")
        elif 'tdel_all' in request.POST:
            # Del item ID
            Del_All = functions.DelCart(request, 'Del_All')
            return HttpResponse(Del_All, content_type="application/json")
        elif 'tsellproduct' in request.POST:
            # Sell Product
            SellProduct = functions.SellingSamsungFinance(request)
            return HttpResponse(SellProduct, content_type="application/json")
        else:
            # Context Default
            context = contexts.Context_Default(request)
            # Add context
            context['Cart'] = objects.Cart(request, 'List', None)
            context['Total_Price'] = objects.Cart(request, 'Total_Price', None)
            context['Members'] = objects.Members(request, None)
            return render(request, 'SamsungFinance.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')

# Sale
def sale(request):
    if request.user.is_authenticated:
        if 'tbarcode' in request.POST:
            # Add items to cart actions
            addcart = functions.AddCart(request)
            return HttpResponse(addcart, content_type="application/json")
        elif 'tdel_id' in request.POST:
            # Del item ID
            Del_id = functions.DelCart(request, 'Del_ID')
            return HttpResponse(Del_id, content_type="application/json")
        elif 'tdel_all' in request.POST:
            # Del item ID
            Del_All = functions.DelCart(request, 'Del_All')
            return HttpResponse(Del_All, content_type="application/json")
        elif 'tsellproduct' in request.POST:
            # Sell Product
            SellProduct = functions.SellingProduct(request)
            return HttpResponse(SellProduct, content_type="application/json")
        else:
            # Context Default
            context = contexts.Context_Default(request)
            # Add context
            context['Cart'] = objects.Cart(request, 'List', None)
            context['Total_Price'] = objects.Cart(request, 'Total_Price', None)
            context['Members'] = objects.Members(request, None)
            return render(request, 'sale.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')    

# Sale-SIM
def sale_sim(request):
    if request.user.is_authenticated:
        return render(request, 'sale-sim.html', contexts.Context_Default(request))
    else:
        return redirect('/เข้าสู่ระบบ/')  

# Top up
def topup(request):
    if request.user.is_authenticated:
        if 'taddphone_number' in request.POST:
            # Add items to cart actions
            addcart = functions.AddCart_Topup(request)
            return HttpResponse(addcart, content_type="application/json")
        elif 'tdel_id' in request.POST:
            # Del item ID
            Del_id = functions.DelCart_Topup(request, 'Del_ID')
            return HttpResponse(Del_id, content_type="application/json")
        elif 'tdel_all' in request.POST:
            # Del item ID
            Del_All = functions.DelCart_Topup(request, 'Del_All')
            return HttpResponse(Del_All, content_type="application/json")
        elif 'tselltopup' in request.POST:
            # Sell Product
            SellTopup = functions.SellingTopup(request)
            return HttpResponse(SellTopup, content_type="application/json")
        else:
            # Context Default
            context = contexts.Context_Default(request)
            # Add context
            context['Cart'] = objects.Cart_Topup(request, 'List', None)
            context['Total_Price'] = objects.Cart_Topup(request, 'Total_Price', None)
            context['Members'] = objects.Members(request, None)
            return render(request, 'topup.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')  

# Invoice
def invoice(request):
    if request.user.is_authenticated:
        # Context Default
        context = contexts.Context_Default(request)
        # Billing context
        context['Billing_Log'] = objects.Billing_Log(request, 'Billing_Log', request.GET.get('get'))
        context['Billing_Detail_Log'] = objects.Billing_Log(request, 'Billing_Detail_Log', request.GET.get('get'))
        context['Billing_Total_Price_Log'] = objects.Billing_Log(request, 'Billing_Total_Price_Log', request.GET.get('get'))
        context['Billing_Change_Log'] = objects.Billing_Log(request, 'Billing_Change_Log', request.GET.get('get'))
        return render(request, 'invoice.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')  

def invoice_print(request):
    if request.user.is_authenticated:
        # Context Default
        context = contexts.Context_Default(request)
        # Billing context
        context['Billing_Log'] = objects.Billing_Log(request, 'Billing_Log', request.GET.get('get'))
        context['Billing_Detail_Log'] = objects.Billing_Log(request, 'Billing_Detail_Log', request.GET.get('get'))
        context['Billing_Total_Price_Log'] = objects.Billing_Log(request, 'Billing_Total_Price_Log', request.GET.get('get'))
        context['Billing_Change_Log'] = objects.Billing_Log(request, 'Billing_Change_Log', request.GET.get('get'))
        return render(request, 'prints/invoice.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')
    
def invoice_topup(request):
    if request.user.is_authenticated:
        # Context Default
        context = contexts.Context_Default(request)
        # Billing context
        context['Billing_Log'] = objects.BillingTopup_Log(request, 'Billing_Log', request.GET.get('get'))
        context['Billing_Detail_Log'] = objects.BillingTopup_Log(request, 'Billing_Detail_Log', request.GET.get('get'))
        context['Billing_Total_Price_Log'] = objects.BillingTopup_Log(request, 'Billing_Total_Price_Log', request.GET.get('get'))
        context['Billing_Change_Log'] = objects.BillingTopup_Log(request, 'Billing_Change_Log', request.GET.get('get'))
        return render(request, 'invoice-topup.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')

def invoice_topup_print(request):
    if request.user.is_authenticated:
        # Context Default
        context = contexts.Context_Default(request)
        # Billing context
        context['Billing_Log'] = objects.BillingTopup_Log(request, 'Billing_Log', request.GET.get('get'))
        context['Billing_Detail_Log'] = objects.BillingTopup_Log(request, 'Billing_Detail_Log', request.GET.get('get'))
        context['Billing_Total_Price_Log'] = objects.BillingTopup_Log(request, 'Billing_Total_Price_Log', request.GET.get('get'))
        context['Billing_Change_Log'] = objects.BillingTopup_Log(request, 'Billing_Change_Log', request.GET.get('get'))
        return render(request, 'prints/invoice-topup.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')

# Cancel Bill    
def cancel_bill(request):
    if request.user.is_authenticated:
        if 'ttype' in request.POST:
            # Add items to cart actions
            cancel_bill = functions.CancelBilling(request)
            return HttpResponse(cancel_bill, content_type="application/json")
        else:
            # Context Default
            context = contexts.Context_Default(request)
            # Add context
            context['Sell_Log'] = objects.Bill_cancel(request, 'Sell_Log')
            context['Topup_Log'] = objects.Bill_cancel(request, 'Topup_Log')
            return render(request, 'cancen-bill.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')
#== End sale System ==#

#== Warehouse ==#

# Store
def store(request):
    if request.user.is_authenticated:
        # Context Default
        context = contexts.Context_Default(request)
        # Add context
        context['Store'] = objects.store(request, None)
        return render(request, 'store.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')
    
# Stock In
def stockin(request):
    if request.user.is_authenticated:
        if 'tget_item' in request.POST:
            # Add items to StockOut actions
            get_item = functions.StockOut(request, 'Get_Item')
            return HttpResponse(get_item, content_type="application/json")
        elif 'tadd_item' in request.POST:
            # Stock Out actions
            stockout = functions.StockOut(request, 'StockOut')
            return HttpResponse(stockout, content_type="application/json")
        else:
            # Context Default
            context = contexts.Context_Default(request)
            # Add context
            context['Product'] = objects.store(request, 'Product')
            return render(request, 'stockin.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')
    
# Stock In
def stockout(request):
    if request.user.is_authenticated:
        if 'tget_item' in request.POST:
            # Add items to Stock Out actions
            addstock_out = functions.AddStockOut(request)
            return HttpResponse(addstock_out, content_type="application/json")
        elif 'tstock_out' in request.POST:
            # Add items to cart actions
            addcart = functions.StockOut(request)
            return HttpResponse(addcart, content_type="application/json")
        elif 'tdel_id' in request.POST:
            # Del item ID
            Del_id = functions.DelStockOut(request, 'Del_ID')
            return HttpResponse(Del_id, content_type="application/json")
        elif 'tdel_all' in request.POST:
            # Del item ID
            Del_All = functions.DelStockOut(request, 'Del_All')
            return HttpResponse(Del_All, content_type="application/json")
        else:     
            # Context Default
            context = contexts.Context_Default(request)
            # Add context
            context['StockOut'] = objects.StockOut(request, 'List', None)
            return render(request, 'stockout.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')
    
def stockout_print(request):
    if request.user.is_authenticated:
        # Context Default
        context = contexts.Context_Default(request)
        # Add context
        context['StockOut'] = objects.StockOut(request, 'List', None)
        context['Total_Count'] = objects.StockOut(request, 'Total_Count', None)
        return render(request, 'prints/stockout.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')
    
# Check Stock
def checkstock(request):
    if request.user.is_authenticated:
        if 'tcreate_stock' in request.POST:
            # Add items to cart actions
            create_stock = functions.CreateStock(request)
            return HttpResponse(create_stock, content_type="application/json")
        elif 'tcheck_stock' in request.POST:
            # Add items to cart actions
            check_stock = functions.CheckStock(request)
            return HttpResponse(check_stock, content_type="application/json")
        else:
            # Context Default
            context = contexts.Context_Default(request)
            # Add context
            context['Stock'] = objects.CheckStock(request, None)
            context['Check_Stock'] = objects.CheckStock(request, True)
            context['Checking_Price'] = objects.CheckStock(request, 'Checking_Price')
            context['Checking_Count'] = objects.CheckStock(request, 'Checking_Count')
            context['Notcheck_Price'] = objects.CheckStock(request, 'Notcheck_Price')
            context['Notcheck_Count'] = objects.CheckStock(request, 'Notcheck_Count')
            return render(request, 'checkstock.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')

def checkstock_print(request):
    if request.user.is_authenticated:
        # Context Default
        context = contexts.Context_Default(request)
        # Add context
        context['Stock'] = objects.CheckStock(request, None)
        context['Check_Stock'] = objects.CheckStock(request, True)
        context['NotCheck_Stock'] = objects.CheckStock(request, False)
        context['Checking_Price'] = objects.CheckStock(request, 'Checking_Price')
        context['Checking_Count'] = objects.CheckStock(request, 'Checking_Count')
        context['Notcheck_Price'] = objects.CheckStock(request, 'Notcheck_Price')
        context['Notcheck_Count'] = objects.CheckStock(request, 'Notcheck_Count')
        return render(request, 'prints/checkstock.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')

#== End Warehouse ==#

#== Report System ==#

# Selling Today
def selling_today(request):
    if request.user.is_authenticated:
        # Context Default
        context = contexts.Context_Default(request)
        # Add context
        context['Sell_Log'] = objects.SellReport(request, 'Sell_Log')
        context['Topup_Log'] = objects.SellReport(request, 'Topup_Log')
        context['Total_Cash'] = objects.SellReport(request, 'Total_Cash')
        context['Total_Transfer'] = objects.SellReport(request, 'Total_Transfer')
        context['Total_Price'] = objects.SellReport(request, 'Total_Price')
        return render(request, 'selling-today.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')
    
def selling_today_print(request):
    if request.user.is_authenticated:
        # Context Default
        context = contexts.Context_Default(request)
        # Add context
        context['Sell_Log'] = objects.SellReport(request, 'Sell_Log')
        context['Topup_Log'] = objects.SellReport(request, 'Topup_Log')
        context['Total_Cash'] = objects.SellReport(request, 'Total_Cash')
        context['Total_Transfer'] = objects.SellReport(request, 'Total_Transfer')
        context['Total_Price'] = objects.SellReport(request, 'Total_Price')
        return render(request, 'prints/selling-today.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')
    
# Selling ToMonth
def selling_tomonth(request):
    if request.user.is_authenticated:
        # Context Default
        context = contexts.Context_Default(request)
        # Add context
        context['Sell_Log'] = objects.SellReport_Month(request, 'Sell_Log')
        context['Topup_Log'] = objects.SellReport_Month(request, 'Topup_Log')
        context['Total_Cash'] = objects.SellReport_Month(request, 'Total_Cash')
        context['Total_Transfer'] = objects.SellReport_Month(request, 'Total_Transfer')
        context['Total_Price'] = objects.SellReport_Month(request, 'Total_Price')
        return render(request, 'selling-tomonth.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')
    
# Selling ToMonth
def selling_tomonth_print(request):
    if request.user.is_authenticated:
        # Context Default
        context = contexts.Context_Default(request)
        # Add context
        context['Sell_Log'] = objects.SellReport_Month(request, 'Sell_Log')
        context['Topup_Log'] = objects.SellReport_Month(request, 'Topup_Log')
        context['Total_Cash'] = objects.SellReport_Month(request, 'Total_Cash')
        context['Total_Transfer'] = objects.SellReport_Month(request, 'Total_Transfer')
        context['Total_Price'] = objects.SellReport_Month(request, 'Total_Price')
        return render(request, 'prints/selling-tomonth.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')
    
# Selling Report    
def selling_report(request):
    if request.user.is_authenticated:
        # Context Default
        context = contexts.Context_Default(request)
        # Add context
        context['Sell_Log'] = objects.Bill_Report(request, 'Sell_Log')
        context['Topup_Log'] = objects.Bill_Report(request, 'Topup_Log')
        return render(request, 'selling-report.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')

#== Report System ==#

#== Members System ==#

# Members
def members(request):
    if request.user.is_authenticated:
        if 'search' in request.POST:
            # Context Default
            context = contexts.Context_Default(request)
            # Add context
            context['Members'] = objects.Members(request, request.POST.get("name", ""))
            return render(request, 'members.html', context)
        else:
            # Context Default
            context = contexts.Context_Default(request)
            # Add context
            context['Members'] = objects.Members(request, None)
            return render(request, 'members.html', context)
    else:
        return redirect('/เข้าสู่ระบบ/')
#== Members System ==#

#== Authenticate ==#

# Login & Logout
def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if 'tlogin' in request.POST:
            # Login actions
            login = functions.Login(request)
            return HttpResponse(login, content_type="application/json")
        else:
            return render(request, 'login.html', contexts.Context_Default(request))

def logout(request):
    functions.Logout(request)
    return redirect('/')

#== End Authenticate ==#
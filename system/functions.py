# Library Global
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.contrib import auth
from datetime import datetime, timedelta
from django.utils import timezone

# Library Models
from django.contrib.auth.models import User
from django.db.models import Sum

# Library App
from . import models, objects
from log import models as models_log

#=== Standard Funcions ===#

# Datetime Format
def Datetime_Format(request, value):
    # Bill log
    bill_con = models_log.Selling_Log.objects.all().count()
    date_now = datetime.now()
    date_fm = date_now.strftime("%Y%b%a%d")
    billing = str(date_fm)+str(bill_con)
    
    if value == 'Billing':
        return billing
    elif value == 'Billing_Detail':
        if bill_con >= 1:
            bill_con2 = bill_con-1
        else:
            bill_con2 = 0
            
        billing_detail = str(date_fm)+str(bill_con2)
        return billing_detail
    else:    
        return billing

#=== End Standard Funcions ===#


#=== Actions Funcions ===#

# Login
def Login(request):
    # Login form
    username = request.POST['tuser']
    password = request.POST['tpass']
    
    if (not username) or (not password):
        return JsonResponse({"status":"N","values":"warning","alertify":"กรุณากรอกรหัสผนักงานและรหัสผ่านเพื่อเข้าสู่ระบบ"})
    else:
        # User validate
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            # Login
            auth.login(request, user)
            # Superuser check
            superuser = request.user.is_superuser
            
            if superuser == True:
                url = "/admin/"
            else:
                url = "/"
            
            return JsonResponse({"status":"Y","url":url})
        else:
            return JsonResponse({"status":"N","values":"error","alertify":"รหัสพนักงานหรือรหัสผ่านไม่ถูกต้อง โปรดลองใหม่อีกครั้ง"})

# Logout
def Logout(request):
    logout = auth.logout(request)
    # Delete session
    request.session.delete()
    return logout

#=== End Actions Funcions ===#

def AddCart(request):
    # Cart form
    barcode = request.POST['tbarcode']
    
    if (not barcode):
        return JsonResponse({"status":"N","alertify":"ไม่พบบาร์โค้ด"})
    else:
        # Get Item
        store = models.Itemlist.objects.filter(item_barcode=barcode, item_id__product_type=1)
        
        if not store:
            return JsonResponse({"status":"N","alertify":"ไม่สามารถขายสินค้านี้ได้เนื่องจาก บาร์โค้ดไม่ถูกต้อง"})
        else:
            # Get Item Check
            item = models.Itemlist.objects.get(item_barcode=barcode)
            
            if item.item_status == "1":
                # Check Cart
                cart_chk = objects.Cart(request, 'Check', barcode)
                
                if cart_chk.exists():
                    return JsonResponse({"status":"N","alertify":"สินค้านี้อยู่ในรายการขายแล้ว"})
                else:
                    # Add Items to Cart
                    add_cart = models.SellProduct(
                        username = request.user.username,
                        barcode_id = barcode,
                        price = item.item_id.product_price
                    )
                    if add_cart:
                        add_cart.save()
                        return JsonResponse({"status":"Y"})
                    else:
                        return JsonResponse({"status":"N","alertify":"เกิดข้อผิดพลาดขณะบันทึกข้อมูล"})
            elif item.item_status == "2":
                return JsonResponse({"status":"N","alertify":"ไม่สามารถขายสินค้านี้ได้เนื่องจาก เป็นสินค้ารอเคลม"})
            elif item.item_status == "3":
                return JsonResponse({"status":"N","alertify":"ไม่สามารถขายสินค้านี้ได้เนื่องจาก เป็นสินค้าโอนออก"})
            elif item.item_status == "4":
                return JsonResponse({"status":"N","alertify":"ไม่สามารถขายสินค้านี้ได้เนื่องจาก สินค้านี้ถูกขายแล้ว"})
            else:
                return JsonResponse({"status":"N","alertify":"ไม่สามารถขายสินค้านี้ได้เนื่องจาก ไม่พบข้อมูล"})
            
def DelCart(request, value):
    if value == 'Del_ID':
        # Cart ID form
        cart_id = request.POST['tid']
        
        if not(cart_id):
            return JsonResponse({"status":"N","alertify":"ไม่พบบาร์โค้ด"})
        else:
            # Cart ID
            del_id = models.SellProduct.objects.get(id=cart_id)
            
            if del_id:
                # Delete Cart ID
                del_id.delete()
                return JsonResponse({"status":"Y"})
            else:
                return JsonResponse({"status":"N","alertify":"ไม่พบสินค้านี้ในรายการขายสินค้า"})
    elif value == 'Del_All':
        # Cart
        del_all = models.SellProduct.objects.filter(username=request.user.username)
        
        if del_all:
            # Delete All Cart
            del_all.delete()
            return JsonResponse({"status":"Y"})
        else:
            return JsonResponse({"status":"N","alertify":"ไม่พบข้อมูลในรายการขายสินค้า"})
    else:
        None
        
# Selling Product
def SellingProduct(request):
    # Selling form
    member = request.POST['tmember']
    ttype = request.POST['ttype']
    cash = request.POST['tcash']
    transfer = request.POST['ttransfer']
    discount = request.POST['tdiscount']
    
    if (not cash.isnumeric()) or (not transfer.isnumeric()):
        return JsonResponse({"status":"N","alertify":"ยังไม่ได้คีย์รับเงินลูกค้า"})
    else:
        if not(cash):
            cash = 0
        elif not(transfer):
            transfer = 0
        elif not(discount):
            discount = 0
            
        # Cart Check
        cart_chk = models.SellProduct.objects.filter(username=request.user.username)
        
        cart_price = models.SellProduct.objects.filter(username=request.user.username).aggregate(Sum('price'))['price__sum']
        cart_total = int(cart_price)-int(discount)
        
        if cart_chk:
            # Add Selling Log
            sell_log = models_log.Selling_Log(
                sell_id = Datetime_Format(request, 'Billing'),
                sell_member = member,
                sell_type = ttype,
                sell_employee = request.user.username,
                cash_money = cash,
                transfer_money = transfer,
                fee = 0,
                discount = discount,
                total_price = cart_total
            )
            if sell_log:
                # Save Billing
                sell_log.save()
                
                sellproduct = models.SellProduct.objects.filter(username=request.user.username)
                for sell in sellproduct:
                    
                    models_log.Sell_Detail_Log(
                        sell_id_id = Datetime_Format(request, 'Billing_Detail'),
                        sell_barcode_id = str(sell.barcode.item_barcode),
                        sell_price = sell.price
                    ).save()
                    
                updatestore = models.SellProduct.objects.filter(username=request.user.username)
                for upstore in updatestore:
                    models.Itemlist.objects.filter(item_barcode = str(upstore.barcode.item_barcode)).update(item_status = 4)
                
                DelCart(request, 'Del_All')
                return JsonResponse({"status":"Y","url":"/ใบเสร็จรับเงิน/?get="+Datetime_Format(request, 'Billing_Detail')})
        else:
            return JsonResponse({"status":"N","alertify":"ไม่พบข้อมูลในรายการขายสินค้า"})
        
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
    bill_con1 = models_log.Topup_Log.objects.all().count()
    bill_sum = int(bill_con)+int(bill_con1)
    date_now = datetime.now()
    date_fm = date_now.strftime("%Y%m%d")
    billing = str(date_fm)+str(bill_sum)
    
    if value == 'Billing':
        return billing
    elif value == 'Billing_Detail':
        if bill_sum >= 1:
            bill_con2 = bill_sum-1
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
    sl_barcode = request.POST['tsl_barcode']
    
    if (not barcode):
        return JsonResponse({"status":"N","alertify":"ไม่พบบาร์โค้ด"})
    else:
        # Get Item
        if sl_barcode == "true":
            store = models.Itemlist.objects.filter(barcode_ean=barcode)
        elif sl_barcode == "false":
            store = models.Itemlist.objects.filter(barcode_aup=barcode)
        
        if not store:
            return JsonResponse({"status":"N","alertify":"ไม่สามารถขายสินค้านี้ได้เนื่องจาก บาร์โค้ดไม่ถูกต้อง"})
        else:
            # Get Item Check
            
            if sl_barcode == "true":
                item = models.Itemlist.objects.get(barcode_ean=barcode)
            elif sl_barcode == "false":
                item = models.Itemlist.objects.get(barcode_aup=barcode)
            
            if item.item_status == "1":
                # Check Cart
                cart_chk = objects.Cart(request, 'Check', item.id)
                
                if cart_chk.exists():
                    return JsonResponse({"status":"N","alertify":"สินค้านี้อยู่ในรายการขายแล้ว"})
                else:
                    # Add Items to Cart
                    add_cart = models.SellProduct(
                        username = request.user.username,
                        barcode_id = item.id,
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
        get_money = int(cash)+int(transfer)
        
        if get_money < cart_total:
            return JsonResponse({"status":"N","alertify":"ยอดเงินรับต่ำกว่าราคาสินค้า"})
        else:
            if cart_chk:
                # Add Selling Log
                sell_log = models_log.Selling_Log(
                    sell_id = Datetime_Format(request, 'Billing'),
                    sell_member_id = member,
                    sell_type = ttype,
                    sell_employee = request.user.username,
                    cash_money = cash,
                    transfer_money = transfer,
                    down_payment = 0,
                    fee = 0,
                    discount = discount,
                    total_price = cart_total,
                    bill_status = 2
                )
                if sell_log:
                    # Save Billing
                    sell_log.save()
                    
                    sellproduct = models.SellProduct.objects.filter(username=request.user.username)
                    for sell in sellproduct:
                        
                        models_log.Sell_Detail_Log(
                            sell_id_id = Datetime_Format(request, 'Billing_Detail'),
                            sell_barcode_id = str(sell.barcode_id),
                            sell_price = sell.price
                        ).save()
                        
                    updatestore = models.SellProduct.objects.filter(username=request.user.username)
                    for upstore in updatestore:
                        models.Itemlist.objects.filter(id = str(upstore.barcode.id)).update(item_status = 4)
                    
                    DelCart(request, 'Del_All')
                    return JsonResponse({"status":"Y","url":"/ใบเสร็จรับเงิน/?get="+Datetime_Format(request, 'Billing_Detail')})
            else:
                return JsonResponse({"status":"N","alertify":"ไม่พบข้อมูลในรายการขายสินค้า"})
        
# Selling SamsungFinance
def SellingSamsungFinance(request):
    # Selling form
    member = request.POST['tmember']
    ttype = request.POST['ttype']
    cash = request.POST['tcash']
    transfer = request.POST['ttransfer']
    down_payment = request.POST['tdown_payment']
    fee = request.POST['tfee']
    
    if (not cash.isnumeric()) or (not transfer.isnumeric()) or (not down_payment.isnumeric()) or (not fee.isnumeric()):
        return JsonResponse({"status":"N","alertify":"ยังไม่ได้คีย์รับเงินลูกค้า"})
    else:
        if not(cash):
            cash = 0
        elif not(transfer):
            transfer = 0
        elif not(down_payment):
            down_payment = 0
        elif not(fee):
            fee = 0
            
        # Cart Check
        cart_chk = models.SellProduct.objects.filter(username=request.user.username)
        cart_total = int(down_payment)+int(fee)
        get_money = int(cash)+int(transfer)
        
        if get_money < cart_total:
            return JsonResponse({"status":"N","alertify":"ยอดเงินรับต่ำกว่าราคาสินค้า"})
        else:
            if cart_chk:
                # Add Selling Log
                sell_log = models_log.Selling_Log(
                    sell_id = Datetime_Format(request, 'Billing'),
                    sell_member_id = member,
                    sell_type = ttype,
                    sell_employee = request.user.username,
                    cash_money = cash,
                    transfer_money = transfer,
                    down_payment = down_payment,
                    fee = fee,
                    discount = 0,
                    total_price = cart_total,
                    bill_status = 1
                )
                if sell_log:
                    # Save Billing
                    sell_log.save()
                    
                    sellproduct = models.SellProduct.objects.filter(username=request.user.username)
                    for sell in sellproduct:
                        
                        models_log.Sell_Detail_Log(
                            sell_id_id = Datetime_Format(request, 'Billing_Detail'),
                            sell_barcode_id = str(sell.barcode_id),
                            sell_price = sell.price
                        ).save()
                        
                    updatestore = models.SellProduct.objects.filter(username=request.user.username)
                    for upstore in updatestore:
                        models.Itemlist.objects.filter(id = str(upstore.barcode.id)).update(item_status = 4)
                    
                    DelCart(request, 'Del_All')
                    return JsonResponse({"status":"Y","url":"/ใบเสร็จรับเงิน/?get="+Datetime_Format(request, 'Billing_Detail')})
            else:
                return JsonResponse({"status":"N","alertify":"ไม่พบข้อมูลในรายการขายสินค้า"})
            
def AddCart_Topup(request):
    # Cart form
    phone_number = request.POST['tphone_number']
    network = request.POST['tnetwork']
    price = request.POST['tprice']
    
    if (not phone_number) or (not network) or (not price):
        return JsonResponse({"status":"N","alertify":"กรอกข้อมูลไม่ครบ"})
    else:
        add_cart_topup = models.Topup(
            username = request.user.username,
            phone_number = phone_number,
            network = network,
            price = price
        )
        if add_cart_topup:
            add_cart_topup.save()
            return JsonResponse({"status":"Y"})
        else:
            return JsonResponse({"status":"N","alertify":"เกิดข้อผิดพลาดขณะบันทึกข้อมูล"})
        
def DelCart_Topup(request, value):
    if value == 'Del_ID':
        # Cart ID form
        cart_id = request.POST['tid']
        
        if not(cart_id):
            return JsonResponse({"status":"N","alertify":"ไม่พบเบอร์โทรศัพท์"})
        else:
            # Cart ID
            del_id = models.Topup.objects.get(id=cart_id)
            
            if del_id:
                # Delete Cart ID
                del_id.delete()
                return JsonResponse({"status":"Y"})
            else:
                return JsonResponse({"status":"N","alertify":"ไม่พบเบอร์โทรศัพท์ในรายการขายสินค้า"})
    elif value == 'Del_All':
        # Cart
        del_all = models.Topup.objects.filter(username=request.user.username)
        
        if del_all:
            # Delete All Cart
            del_all.delete()
            return JsonResponse({"status":"Y"})
        else:
            return JsonResponse({"status":"N","alertify":"ไม่พบเบอร์โทรศัพท์ในรายการขายสินค้า"})
    else:
        None
        
# Selling Topup
def SellingTopup(request):
    # Selling form
    member = request.POST['tmember']
    cash = request.POST['tcash']
    transfer = request.POST['ttransfer']
    fee = request.POST['tfee']
    
    if (not cash.isnumeric()) or (not transfer.isnumeric()) or (not fee.isnumeric()):
        return JsonResponse({"status":"N","alertify":"ยังไม่ได้คีย์รับเงินลูกค้า"})
    else:
        if not(cash):
            cash = 0
        elif not(transfer):
            transfer = 0
        elif not(fee):
            fee = 0
            
        # Cart Check
        cart_chk = models.Topup.objects.filter(username=request.user.username)
        cart_total = int(objects.Cart_Topup(request, 'Total_Price', None))+int(fee)
        get_money = int(cash)+int(transfer)
        
        if get_money < cart_total:
            return JsonResponse({"status":"N","alertify":"ยอดเงินรับต่ำกว่าราคาสินค้า"})
        else:
            if cart_chk:
                topup_log = models_log.Topup_Log(
                    topup_id = Datetime_Format(request, 'Billing'),
                    topup_member_id = member,
                    topup_type = 1,
                    topup_employee = request.user.username,
                    cash_money = cash,
                    transfer_money = transfer,
                    fee = fee,
                    discount = 0,
                    total_price = cart_total
                )
                
                if topup_log:
                    # Save Billing
                    topup_log.save()
                    
                    selltopup = models.Topup.objects.filter(username=request.user.username)
                    for sell in selltopup:
                        
                        models_log.Topup_Detail_Log(
                            topup_id_id = Datetime_Format(request, 'Billing_Detail'),
                            phone_number = sell.phone_number,
                            network = sell.network,
                            price = sell.price
                        ).save()
                        
                    DelCart_Topup(request, 'Del_All')
                    return JsonResponse({"status":"Y","url":"/ใบเสร็จรับเงิน-เติมเงิน/?get="+Datetime_Format(request, 'Billing_Detail')})
            else:
                return JsonResponse({"status":"N","alertify":"ไม่พบข้อมูลในรายการขายสินค้า"})
            
# Cancel Billing
def CancelBilling(request):
    # Billing form
    bill_type = request.POST['ttype']
    bill_id = request.POST['tid']
    
    if bill_type == "sell":
        # Selling Detail Log
        sell_detail_log = models_log.Sell_Detail_Log.objects.filter(sell_id=bill_id)
        for sell in sell_detail_log:
            models.Itemlist.objects.filter(id=sell.sell_barcode.id).update(item_status=1)
            
        # Selling Log
        cancel_bill = models_log.Selling_Log.objects.filter(sell_id=bill_id).update(active=False)
        if cancel_bill:
            return JsonResponse({"status":"Y","url":"/ยกเลิกบิล/"})
        else:
            return JsonResponse({"status":"N","alertify":"เกิดข้อผิดพลาดขณะบันทึกข้อมูล"})
    elif bill_type == "topup":
        # Topup Log
        cancel_topup = models_log.Topup_Log.objects.filter(topup_id=bill_id).update(active=False)
        if cancel_topup:
            return JsonResponse({"status":"Y","url":"/ยกเลิกบิล/"})
        else:
            return JsonResponse({"status":"N","alertify":"เกิดข้อผิดพลาดขณะบันทึกข้อมูล"})
    else:
        return JsonResponse({"status":"N","alertify":"ไม่พบข้อมูลบิลใบเสร็จ"})
    
# Stock IN
def StockIn(request):
    # StockIn form
    product_id = request.POST['tproduct_id']
    bc_ean = request.POST['tbc_ean']
    bc_aup = request.POST['tbc_aup']
    imei1 = request.POST['timei1']
    imei2 = request.POST['timei2']
    imei3 = request.POST['timei3']
    
    if (not product_id) or (not bc_ean):
        return JsonResponse({"status":"N","alertify":"โปรดเลือกสินค้าที่ต้องการรับเข้าและสแกนบาร์โค้ดสินค้า"})
    else:
        # Check Store
        store = models.Itemlist.objects.filter(barcode_aup=bc_aup)
        
        if store:
            return JsonResponse({"status":"N","alertify":"บาร์โค้ดแอดไวซ์ซ้ำกับสินค้าในคลัง"})
        else:
            add_item = models.Itemlist(
                item_id_id = product_id,
                barcode_ean = bc_ean,
                barcode_imei1 = imei1,
                barcode_imei2 = imei2,
                barcode_imei3 = imei3,
                barcode_aup = bc_aup,
                item_status = 1
            )
            if add_item:
                # Save Item
                add_item.save()
                return JsonResponse({"status":"Y","url":"/รับสินค้า/"})
            else:
                return JsonResponse({"status":"N","alertify":"เกิดข้อผิดพลาดขณะบันทึกข้อมูล"})
            
# Add Product
def AddProdect(request):
    # Add Product form
    item_name = request.POST['titem_name']
    item_id = request.POST['titem_id']
    item_price = request.POST['titem_price']
    item_network = request.POST['titem_network']
    item_type = request.POST['titem_type']
    
    if (not item_name) or (not item_id) or (not item_price) or (not item_network) or (not item_type):
        return JsonResponse({"status":"N","alertify":"โปรดกรอกข้อมูลให้ครบทุกช่อง"})
    else:
        # Check Store
        store = models.Products.objects.filter(product_id=item_id)
        
        if store:
            return JsonResponse({"status":"N","alertify":"มีรหัสสินค้านี้ในคลังสินค้า"})
        else:
            add_product = models.Products(
                product_id = item_id,
                product_name = item_name,
                product_network = item_network,
                product_price = item_price,
                product_type = item_type
            )
            if add_product:
                # Save Item
                add_product.save()
                return JsonResponse({"status":"Y","url":"/รับสินค้า/"})
            else:
                return JsonResponse({"status":"N","alertify":"เกิดข้อผิดพลาดขณะบันทึกข้อมูล"})
    
# Create Stock
def CreateStock(request):
    store = models.Itemlist.objects.filter(item_status=1)
    
    if store:
        stock = models.CheckStock.objects.all()
        if stock:
            stock.delete()
            for item in store:
                models.CheckStock(
                    username = request.user.username,
                    barcode_id = item.id,
                    price = item.item_id.product_price,
                    count = 1
                ).save()
            return JsonResponse({"status":"Y","url":"/เช็คสต๊อก/"})
        else:
            for item in store:
                models.CheckStock(
                    username = request.user.username,
                    barcode_id = item.id,
                    price = item.item_id.product_price,
                    count = 1
                ).save()
            return JsonResponse({"status":"Y","url":"/เช็คสต๊อก/"})
    else:
        return JsonResponse({"status":"N","alertify":"ไม่พบสินค้าในคลังสินค้า"})
    
# Check Stock
def CheckStock(request):
    # Stock form
    barcode = request.POST['tbarcode']
    sl_barcode = request.POST['tsl_barcode']
    
    if (not barcode):
        return JsonResponse({"status":"N","alertify":"ไม่พบบาร์โค้ด"})
    else:
        # Get Item
        if sl_barcode == "true":
            stock = models.CheckStock.objects.filter(barcode__barcode_ean=barcode)
        elif sl_barcode == "false":
            stock = models.CheckStock.objects.filter(barcode__barcode_aup=barcode)
        
        if not stock:
            return JsonResponse({"status":"N","alertify":"บาร์โค้ดไม่ถูกต้อง"})
        else:
            # Get Item Check
            if sl_barcode == "true":
                item = models.CheckStock.objects.get(barcode__barcode_ean=barcode)
                if item.active == True:
                    return JsonResponse({"status":"N","alertify":"สินค้าถูกเช็คแล้ว"})
                else:
                    models.CheckStock.objects.filter(barcode__barcode_ean=barcode).update(active=True)
            elif sl_barcode == "false":
                item = models.CheckStock.objects.get(barcode__barcode_aup=barcode)
                if item.active == True:
                    return JsonResponse({"status":"N","alertify":"สินค้าถูกเช็คแล้ว"})
                else:
                    models.CheckStock.objects.filter(barcode__barcode_aup=barcode).update(active=True)
            return JsonResponse({"status":"Y","url":"/เช็คสต๊อก/"})
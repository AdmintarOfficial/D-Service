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
    # Sale form
    barcode = request.POST['tbarcode']
    
    if (not barcode):
        return JsonResponse({"status":"N","alertify":"ไม่พบบาร์โค้ด"})
    else:
        # Add Items to Cart
        add_cart = models.SellProduct(
            sell_barcode_id = barcode
        )
        
        if add_cart:
            add_cart.save()
            return JsonResponse({"status":"Y"})
        else:
            return JsonResponse({"status":"N","alertify":"เกิดข้อผิดพลาดขณะบันทึกข้อมูล"})
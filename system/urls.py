# Library Global
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

# Library App
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ซัมซุงไฟแนนซ์/', views.samsungfinance, name='SamsungFinance'),
    path('ขายสินค้า/', views.sale, name='Sale'),
    path('ขายซิม/', views.sale_sim, name='Sale-SIM'),
    path('เติมเงินออนไลน์/', views.topup, name='Top-up'),
    path('ใบเสร็จรับเงิน/', views.invoice, name='Invoice'),
    path('ใบเสร็จรับเงิน-ปริ้น/', views.invoice_print, name='Invoice-Print'),
    path('ใบเสร็จรับเงิน-เติมเงิน/', views.invoice_topup, name='Invoice-Topup'),
    path('ใบเสร็จรับเงิน-เติมเงิน-ปริ้น/', views.invoice_topup_print, name='Invoice-Topup-Print'),
    path('คืนสินค้า/', views.index, name='Product-return'),
    path('เคลมสินค้า/', views.index, name='Product-Claim'),
    path('คลังสินค้า/', views.store, name='Store'),
    path('รับสินค้า/', views.index, name='Product-Add'),
    path('โอนสินค้า/', views.index, name='Product-Transfer'),
    path('เช็คสต๊อก/', views.checkstock, name='checkstock'),
    path('เช็คสต๊อก-ปริ้น/', views.checkstock_print, name='checkstock-Print'),
    path('ยอดผ่อนมือถือ/', views.index, name='SamsungFinance-log'),
    path('ยอดขายสินค้า/', views.index, name='Sale-log'),
    path('ยอดขายซิม/', views.index, name='Sale-SIM-log'),
    path('ยอดเติมเงินออนไลน์/', views.index, name='Top-up-log'),
    path('การเช็คสต๊อก/', views.index, name='checkstock-log'),
    path('โปรโมชั่น/', views.index, name='Promotion'),
    path('สมาชิกร้าน/', views.members, name='Members'),
    path('พนักงาน/', views.index, name='Employee'),
    path('ตั้งค่าระบบ/', views.index, name='Setting'),
    path('เข้าสู่ระบบ/', views.login, name='Login'),
    path('ออกจากระบบ/', views.logout, name='Logout')
]
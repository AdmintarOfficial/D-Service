# Library Global
from django.db import models

# Library App
from system import models as System_db

# Create your models here.

# Selling Log
class Selling_Log(models.Model):
    type = (
        ('1', 'รับหน้าร้าน'),
        ('2', 'นอกสถานที่'),
        ('3', 'จัดส่ง')
    )
    status = (
        ('1', 'ซัมซุงไฟแนนซ์'),
        ('2', 'ขายสินค้า')
    )
    sell_id = models.CharField(max_length=20, unique=True)
    sell_member = models.ForeignKey(System_db.Members, on_delete=models.CASCADE, blank=True, null=True)
    sell_type = models.CharField(max_length=1, choices=type)
    sell_employee = models.CharField(max_length=100)
    cash_money = models.DecimalField(max_digits=8, decimal_places=2)
    transfer_money = models.DecimalField(max_digits=8, decimal_places=2)
    down_payment = models.DecimalField(max_digits=8, decimal_places=2)
    fee = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True)
    bill_status = models.CharField(max_length=1, choices=status)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Selling_Log"
        verbose_name_plural = "Selling Log"
        
    def __str__(self):
        return self.sell_id
    
# Selling Detail Log
class Sell_Detail_Log(models.Model):
    sell_id = models.ForeignKey(Selling_Log, to_field='sell_id', on_delete=models.CASCADE)
    sell_barcode = models.ForeignKey(System_db.Itemlist, on_delete=models.CASCADE)
    sell_count = models.IntegerField(default=1)
    sell_price = models.DecimalField(max_digits=8, decimal_places=2)
    
    class Meta:
        verbose_name = "Sell_Detail_Log"
        verbose_name_plural = "Sell Detail Log"
        
    def __str__(self):
        return self.sell_barcode.item_id.product_name
    
# Topup Log
class Topup_Log(models.Model):
    type = (
        ('1', 'รับหน้าร้าน'),
        ('2', 'นอกสถานที่'),
        ('3', 'จัดส่ง')
    )
    topup_id = models.CharField(max_length=20, unique=True)
    topup_member = models.ForeignKey(System_db.Members, on_delete=models.CASCADE, blank=True, null=True)
    topup_type = models.CharField(max_length=1, choices=type)
    topup_employee = models.CharField(max_length=100)
    cash_money = models.DecimalField(max_digits=8, decimal_places=2)
    transfer_money = models.DecimalField(max_digits=8, decimal_places=2)
    fee = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Topup_Log"
        verbose_name_plural = "Topup Log"
        
    def __str__(self):
        return self.topup_id
    
# Topup Detail Log
class Topup_Detail_Log(models.Model):
    network = (
        ('0', 'ไม่มี'),
        ('1', 'AIS'),
        ('2', 'DTAC'),
        ('3', 'TrueMove'),
        ('4', 'TOT'),
        ('5', 'CAT')
    )
    topup_id = models.ForeignKey(Topup_Log, to_field='topup_id', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    network = models.CharField(max_length=1, choices=network)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    class Meta:
        verbose_name = "Topup_Detail_Log"
        verbose_name_plural = "Topup Detail Log"
        
    def __str__(self):
        return self.phone_number
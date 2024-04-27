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
    sell_id = models.CharField(max_length=20, unique=True)
    sell_member = models.CharField(max_length=100)
    sell_type = models.CharField(max_length=1, choices=type)
    sell_employee = models.CharField(max_length=100)
    cash_money = models.DecimalField(max_digits=8, decimal_places=2)
    transfer_money = models.DecimalField(max_digits=8, decimal_places=2)
    fee = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Selling_Log"
        verbose_name_plural = "Selling Log"
        
    def __str__(self):
        return self.sell_id
    
# Selling Detail Log
class Sell_Detail_Log(models.Model):
    sell_id = models.ForeignKey(Selling_Log, to_field='sell_id', on_delete=models.CASCADE)
    sell_barcode = models.ForeignKey(System_db.Itemlist, to_field='item_barcode', on_delete=models.CASCADE)
    sell_count = models.IntegerField(default=1)
    sell_price = models.FloatField()
    
    class Meta:
        verbose_name = "Sell_Detail_Log"
        verbose_name_plural = "Sell Detail Log"
        
    def __str__(self):
        return self.sell_barcode.item_id.product_name
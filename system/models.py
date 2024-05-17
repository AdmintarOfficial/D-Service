from django.db import models

# Create your models here.

# Products
class Products(models.Model):
    type = (
        ('1', 'สมาร์ทโฟน'),
        ('2', 'แท็บเล็ต'),
        ('3', 'ซิม'),
        ('4', 'อุปกรณ์เสริม')
    )
    network = (
        ('0', 'ไม่มี'),
        ('1', 'AIS'),
        ('2', 'DTAC'),
        ('3', 'TrueMove'),
        ('4', 'TOT'),
        ('5', 'CAT')
    )
    product_id = models.CharField(max_length=20, unique=True)
    product_img = models.ImageField(upload_to='Product_pic', blank=True, null=True)
    product_name = models.CharField(max_length=100)
    product_detail = models.CharField(max_length=100, blank=True, null=True)
    product_network = models.CharField(max_length=1, choices=network)
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
    product_type = models.CharField(max_length=1, choices=type)
    
    class Meta:
        verbose_name = "Products"
        verbose_name_plural = "Products"
        
    def __str__(self):
        return self.product_name
    
# Itemlist
class Itemlist(models.Model):
    status = (
        ('1', 'พร้อมขาย'),
        ('2', 'รอเคลม'),
        ('3', 'โอนออก'),
        ('4', 'ขายแล้ว')
    )
    item_id  = models.ForeignKey(Products, on_delete=models.CASCADE)
    barcode_ean = models.CharField(max_length=20, blank=True, null=True)
    barcode_imei1 = models.CharField(max_length=20, blank=True, null=True)
    barcode_imei2 = models.CharField(max_length=20, blank=True, null=True)
    barcode_imei3 = models.CharField(max_length=20, blank=True, null=True)
    barcode_aup = models.CharField(max_length=20, blank=True, null=True, unique=True)
    item_regis = models.DateTimeField(auto_now_add=True)
    item_status = models.CharField(max_length=1, choices=status)
    datetime = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name = "ItemList"
        verbose_name_plural = "Item List"
        
    def __str__(self):
        return self.item_id.product_name
    
#== Selling System ==#
    
# Sell Product
class SellProduct(models.Model):
    username = models.CharField(max_length=20)
    barcode = models.ForeignKey(Itemlist, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    class Meta:
        verbose_name = "SellProduct"
        verbose_name_plural = "Sell Product"
        
    def __str__(self):
        return self.barcode.item_id.product_name
    

# Topup
class Topup(models.Model):
    network = (
        ('0', 'ไม่มี'),
        ('1', 'AIS'),
        ('2', 'DTAC'),
        ('3', 'TrueMove'),
        ('4', 'TOT'),
        ('5', 'CAT')
    )
    username = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=10)
    network = models.CharField(max_length=1, choices=network)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    class Meta:
        verbose_name = "SellTopup"
        verbose_name_plural = "Sell Topup"
        
    def __str__(self):
        return self.phone_number
    
#== End Selling System ==#

#== Store System ==#

# Stock Out
class StockOut(models.Model):
    username = models.CharField(max_length=20)
    barcode = models.ForeignKey(Itemlist, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    
    class Meta:
        verbose_name = "StockOut"
        verbose_name_plural = "Stock Out"
        
    def __str__(self):
        return self.barcode.item_id.product_name
    
# Check Stock
class CheckStock(models.Model):
    username = models.CharField(max_length=20)
    barcode = models.ForeignKey(Itemlist, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    count = models.IntegerField(default=1)
    active = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "CheckStock"
        verbose_name_plural = "Check Stock"
        
    def __str__(self):
        return self.barcode.item_id.product_name

#== End Store System ==#

#== Members System ==#

# Members
class Members((models.Model)):
    sex = (
        ('1', 'male'),
        ('2', 'female')
    )
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=sex, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Members"
        verbose_name_plural = "Members"
        
    def __str__(self):
        return self.first_name

#== Members System ==#
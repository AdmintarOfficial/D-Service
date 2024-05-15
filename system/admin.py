from django.contrib import admin

from . import models

# Register your models here.

# Products
admin.site.register(models.Products)
admin.site.register(models.Itemlist)

#== Selling System ==#
admin.site.register(models.SellProduct)
admin.site.register(models.Topup)
#== End Selling System ==#

#== Store System ==#
admin.site.register(models.StockOut)
admin.site.register(models.CheckStock)
#== End Store System ==#

#== Members System ==#
admin.site.register(models.Members)
#== End Members System ==#


from django.contrib import admin

from . import models

# Register your models here.

# Products
admin.site.register(models.Products)
admin.site.register(models.Itemlist)

#== Selling System ==#
admin.site.register(models.SellProduct)
#== End Selling System ==#

#== Members System ==#
admin.site.register(models.Members)
#== End Members System ==#


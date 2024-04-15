from django.shortcuts import render

from . import contexts

# Create your views here.

#== sale System ==#

# Index
def index(request):
    return render(request, 'index.html', contexts.Context_Default(request))

# SamsungFinance
def samsungfinance(request):
    return render(request, 'SamsungFinance.html', contexts.Context_Default(request))

# Sale
def sale(request):
    return render(request, 'sale.html', contexts.Context_Default(request))

# Sale-SIM
def sale_sim(request):
    return render(request, 'sale-sim.html', contexts.Context_Default(request))

# Top up
def topup(request):
    return render(request, 'topup.html', contexts.Context_Default(request))

# Invoice
def invoice(request):
    return render(request, 'invoice.html', contexts.Context_Default(request))

def invoice_print(request):
    return render(request, 'prints/invoice.html', contexts.Context_Default(request))


#== End sale System ==#

#== Warehouse ==#

# Store
def store(request):
    return render(request, 'store.html', contexts.Context_Default(request))

# Check Stock
def checkstock(request):
    return render(request, 'checkstock.html', contexts.Context_Default(request))

def checkstock_print(request):
    return render(request, 'prints/checkstock.html', contexts.Context_Default(request))


#== End Warehouse ==#

#== Members System ==#

# Members
def members(request):
    return render(request, 'members.html', contexts.Context_Default(request))



#== Members System ==#

#== Authenticate ==#

# Login
def login(request):
    return render(request, 'login.html', contexts.Context_Default(request))

#== End Authenticate ==#
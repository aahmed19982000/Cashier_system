from django.shortcuts import render

# Create your views here.

def pos_page(request):
    return render(request, 'pos/pos_page.html')



def menu_management(request):
    return render(request, 'pos/menu_management.html')



def inventory_management(request):
    return render(request, 'pos/inventory_management.html')


def sales_reports(request):
    return render(request, 'pos/sales_reports.html')


def customer_management(request):
    return render(request, 'pos/customer_management.html')


def employees_management(request):
    return render(request, 'pos/employees_management.html')
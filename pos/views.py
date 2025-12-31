from django.shortcuts import render
from .models import Product
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from django.contrib import messages
from categories.models import Category_products
# Create your views here.


def pos_page(request):
    # جلب جميع المنتجات المتاحة
    products = Product.objects.filter(available=True)
    # جلب جميع التصنيفات لعرضها في الفلاتر
    categories = Category_products.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'pos/pos_page.html', context)



def menu_management(request, product_id=None):
    """
    إدارة المنيو: إضافة، تعديل، حذف
    """
    if product_id:
        product = get_object_or_404(Product, id=product_id)
    else:
        product = None

    # عملية الإضافة أو التعديل
    if request.method == 'POST':
        if 'delete' in request.POST and product:
            product.delete()
            messages.success(request, 'تم حذف المنتج بنجاح!')
            return redirect('menu_management')

        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            if product:
                messages.success(request, 'تم تعديل المنتج بنجاح!')
            else:
                messages.success(request, 'تم إضافة المنتج بنجاح!')
            return redirect('menu_management')
        else:
            messages.error(request, 'هناك خطأ في البيانات، يرجى التحقق.')
    else:
        form = ProductForm(instance=product)

    products = Product.objects.all()
    return render(request, 'pos/menu_management.html', {
        'form': form,
        'products': products,
        'editing_product': product
    })




def inventory_management(request):
    return render(request, 'pos/inventory_management.html')


def sales_reports(request):
    return render(request, 'pos/sales_reports.html')


def customer_management(request):
    return render(request, 'pos/customer_management.html')


def employees_management(request):
    return render(request, 'pos/employees_management.html')
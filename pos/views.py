from django.shortcuts import render
from .models import Product
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from django.contrib import messages
from categories.models import Category_products
from django.contrib.auth import get_user_model
from accounts.decorators import role_required

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem , Status_order
from django.db.models import Sum, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta


# Create your views here.




@csrf_exempt
@login_required
def cash_checkout(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        cart = data.get('cart', [])
        total = data.get('total')

        order = Order.objects.create(
            user=request.user,
            payment_method='cash',
            total_price=total
        )

        for item in cart:
            product = Product.objects.get(id=item['id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                price=item['price'],
                quantity=item['qty']
            )

        return JsonResponse({
            'status': 'success',
            'order_id': order.id
        })



@login_required
def pos_page(request):
    # جلب جميع المنتجات المتاحة
    products = Product.objects.filter(available=True)
    # جلب جميع التصنيفات لعرضها في الفلاتر
    categories = Category_products.objects.all()

    #تنفيذ الطلبات في السلة 

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'pos/pos_page.html', context)


@role_required('manager')
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





User = get_user_model()

def sales_reports(request):
    user = request.user
    now = timezone.now()
    
    # 1. جلب بارامترات الفلترة من الرابط (GET)
    filter_type = request.GET.get('range', 'today')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    staff_id = request.GET.get('staff_id', 'all')
    selected_status = request.GET.get('status_id', 'all')
    
    # 2. بناء استعلام التاريخ (Date Filter Query)
    query_date = Q()
    if filter_type == 'today':
        query_date &= Q(created_at__date=now.date())
    elif filter_type == 'week':
        query_date &= Q(created_at__gte=now - timedelta(days=7))
    elif filter_type == 'month':
        query_date &= Q(created_at__month=now.month, created_at__year=now.year)
    elif filter_type == 'custom' and start_date and end_date:
        query_date &= Q(created_at__date__gte=start_date, created_at__date__lte=end_date)
    elif selected_status and selected_status != 'all':
        query_date &= Q(status_id=selected_status)

    # 3. إدارة الصلاحيات وفلتر الموظفين
    staff_members = None
    selected_staff_name = None
    
    # التحقق مما إذا كان المستخدم مديراً (Manager)
    if hasattr(user, 'role') and user.role == 'manager':
        is_manager = True
        # جلب جميع المستخدمين ليعرضهم المدير في القائمة المنسدلة
        staff_members = User.objects.all() 
        
        # إذا اختار المدير موظفاً معيناً من القائمة
        if staff_id and staff_id != 'all':
            query_date &= Q(user_id=staff_id)
            staff_obj = User.objects.filter(id=staff_id).first()
            if staff_obj:
                selected_staff_name = staff_obj.get_full_name() or staff_obj.username
    else:
        # إذا كان موظفاً عادياً، تظهر بياناته هو فقط ولا يمكنه تغيير الفلتر
        is_manager = False
        query_date &= Q(user=user)

    # 4. جلب الطلبات بناءً على الفلترة النهائية
    report_orders = Order.objects.filter(query_date)
    all_statuses = Status_order.objects.all()
    
    # 5. حساب الإحصائيات المالية
    stats = {
        'total_sales': report_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0,
        'orders_count': report_orders.count(),
        'avg_order': report_orders.aggregate(Avg('total_price'))['total_price__avg'] or 0,
    }

    # 6. الأصناف الأكثر مبيعاً (Top 5)
    best_sellers = OrderItem.objects.filter(order__in=report_orders) \
        .values('product__name') \
        .annotate(total_qty=Sum('quantity')) \
        .order_by('-total_qty')[:5]

    # 7. تجهيز السياق للقالب (Template Context)
    context = {
        'stats': stats,
        'best_sellers': best_sellers,
        'recent_orders': report_orders.prefetch_related('items__product').order_by('-created_at')[:10],
        'is_manager': is_manager,
        'staff_members': staff_members,
        'selected_staff': staff_id,
        'selected_staff_name': selected_staff_name,
        'filter_type': filter_type,
        'now': now,
        'all_statuses': all_statuses,
        'selected_status': selected_status,
    }
    
    return render(request, 'pos/sales_reports.html', context)


def customer_management(request):
    return render(request, 'pos/customer_management.html')


def employees_management(request):
    return render(request, 'pos/employees_management.html')






User = get_user_model()

def orders(request):
    user = request.user
    staff_members = None
    
    if hasattr(user, 'role') and user.role == 'manager':
        # المدير يرى كل الطلبات وكل الموظفين
        all_orders = Order.objects.all().prefetch_related('items__product').order_by('-created_at')
        total_sales = all_orders.aggregate(Sum('total_price'))['total_price__sum']
        staff_members = User.objects.all() # جلب الموظفين للفلتر
    else:
        # الموظف يرى طلباته فقط
        all_orders = Order.objects.filter(user=user).prefetch_related('items__product').order_by('-created_at')
        total_sales = all_orders.aggregate(Sum('total_price'))['total_price__sum']

    context = {
        'orders': all_orders,
        'total_sales': total_sales or 0,
        'staff_members': staff_members, # إرسال الموظفين للقالب
    }
    return render(request, 'pos/orders.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # التحقق من الصلاحيات: الموظف يرى طلباته فقط، المدير يرى الكل
    if request.user.role != 'manager' and order.user != request.user:
        messages.error(request, "ليس لديك صلاحية للوصول لهذا الطلب")
        return redirect('orders')
    
    return render(request, 'pos/order_detail.html', {'order': order})




@login_required
def process_order_action(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    action = request.POST.get('action')
    # تأكد من أن حقل role موجود في موديل المستخدم لديك
    user_role = getattr(request.user, 'role', 'staff') 

    if action == 'return':
        # استخدام حقل status بدلاً من name بناءً على بنية الموديل لديك
        try:
            # سنحاول جلب الحالة التي تحتوي على كلمة "مرتجع"
            returned_status = Status_order.objects.filter(status__icontains="مرتجع").first()
            
            if returned_status:
                order.status = returned_status
                order.save()
                messages.success(request, f"تم إرجاع الطلب #{order.id} بنجاح")
            else:
                messages.error(request, "لم يتم العثور على حالة باسم 'مرتجع' في قاعدة البيانات")
        except Exception as e:
            messages.error(request, f"خطأ فني: {str(e)}")

    elif action == 'delete':
        if user_role == 'manager':
            order.delete()
            messages.success(request, "تم حذف الطلب نهائياً")
            return redirect('orders') # تأكد من وجود رابط بهذا الاسم في urls.py
        else:
            messages.error(request, "عذراً، صلاحية الحذف للمدير فقط")

    elif action == 'edit_payment':
        if user_role == 'manager':
            new_method = request.POST.get('payment_method')
            if new_method in ['cash', 'visa']:
                order.payment_method = new_method
                order.save()
                messages.success(request, "تم تحديث طريقة الدفع بنجاح")
            else:
                messages.error(request, "طريقة دفع غير صالحة")
        else:
            messages.error(request, "عذراً، صلاحية التعديل للمدير فقط")

    return redirect('order_detail', order_id=order.id)
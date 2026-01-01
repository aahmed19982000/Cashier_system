from django.urls import path
from . import views


urlpatterns = [
    path('', views.pos_page, name='pos_page'),
    path('menu/', views.menu_management, name='menu_management'),
    path('inventory/', views.inventory_management, name='inventory_management'),
    path('sales-reports/', views.sales_reports, name='sales_reports'),
    path('customer-management/', views.customer_management, name='customer_management'),
    path('employees-management/', views.employees_management, name='employees_management'),
    path('menu/<int:product_id>/', views.menu_management, name='menu_management'),
    path('checkout/cash/', views.cash_checkout, name='cash_checkout'),
    path('orders/', views.orders, name='orders'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('<int:order_id>/action/', views.process_order_action, name='process_order_action'),






    


]

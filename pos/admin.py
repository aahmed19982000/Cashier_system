# admin.py
from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available')  # الأعمدة اللي تظهر في القائمة
    list_filter = ('available',)                   # فلتر حسب التوافر
    search_fields = ('name',)                      # البحث حسب الاسم
    list_editable = ('price', 'available')        # تعديل مباشر في القائمة

# تسجيل الموديل مع الـ admin
admin.site.register(Product, ProductAdmin)

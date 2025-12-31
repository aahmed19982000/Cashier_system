from django.db import models
from categories.models import Category_products

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم المنتج")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
    available = models.BooleanField(default=True, verbose_name="متاح")
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")
    Category = models.ForeignKey(Category_products,on_delete=models.CASCADE,verbose_name="التصنيف",null=True,blank=True)

    def __str__(self):
        return self.name


from django.shortcuts import render 
from django.contrib.auth.decorators import login_required 
from accounts.decorators import role_required
from django.utils import timezone
from django.db.models import Count, Q , F, Value
from django.utils.timezone import localdate
from django.db.models.functions import Concat




#صفحة لوحة التحكم 
def dashboard_view(request):
   

    return render(request, 'home/dashboard.html')
# views.py

#لوحة تحكم الموظف
@login_required
def employee_dashboard(request):
    


    return render(request, 'home/employee_dashboard.html', {
    
    })

# لوحة تحكم المصمم
@login_required
def designer_dashboard(request):
   

    return render(request, 'home/designer_dashboard.html', {
    })

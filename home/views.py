from django.shortcuts import render 
from django.contrib.auth.decorators import login_required 
from accounts.decorators import role_required
from django.utils import timezone
from django.db.models import Count, Q , F, Value
from django.utils.timezone import localdate
from django.db.models.functions import Concat




#صفحة لوحة التحكم 
@role_required('manager')
def dashboard_view(request):
   

    return render(request, 'home/dashboard.html')
# views.py

#لوحة تحكم الموظف
@login_required
def employee_dashboard(request):
    user = request.user
    tasks = Task.objects.filter(writer=user)
    today = localdate()  # بدل date.today()

    total = tasks.count()
    completed = tasks.filter(status__in=['done','upload']).count()
    completed_publish= tasks.filter(status__in=['publish']).count()
    pending = tasks.filter(status__in=['in_progress']).count()
    total_finished = completed + completed_publish
    progress_percent = int((total_finished / total) * 100) if total > 0 else 0

    # ✅ المهام المطلوبة اليوم
    todays_tasks = tasks.filter(publish_date=today)

    # ✅ المهام المؤخرة (قبل اليوم ولم تُنجز)
    overdue_tasks = tasks.filter(publish_date__lt=today).exclude(status__in=['done', 'publish','upload'])

    #اخر  مقالات تحتاج الي صور تم ارسالها للمصمم
    tasks_image = tasks.filter(is_need_image="YES")
    image_in_progress = tasks_image.filter(image_status__in=['in_progress'])
    image_in_send = tasks_image.filter(image_status__in=['send'])


    return render(request, 'home/employee_dashboard.html', {
        'total_tasks': total,
        'completed_tasks': completed,
        'completed_publish' : completed_publish,
        'pending_tasks': pending,
        'progress_percent': progress_percent,
        'todays_tasks': todays_tasks,
        'overdue_tasks': overdue_tasks,
        'image_in_progress': image_in_progress,
        'image_in_send' : image_in_send,
        
    })

# لوحة تحكم المصمم
@login_required
def designer_dashboard(request):
    tasks = Task.objects.filter(is_need_image="YES")

    # العدد الكلي
    total = tasks.count()

    # المهام المرسلة
    sent = tasks.filter(image_status='send').count()

    # المهام المنشورة (منجزة)
    published = tasks.filter(image_status='publish').count()

    # المهام الجاري العمل عليها (QuerySet مش عدد)
    in_progress = tasks.filter(image_status='in_progress')

    # مجموع المهام المنجزة (المرسلة + المنشورة)
    completed = sent + published  

    # المتبقية = الكلي - (منجزة + جاري العمل)
    pending = total - (completed + in_progress.count())

    # نسبة الإنجاز (منجزة ÷ كلي)
    progress_percent = int((completed / total) * 100) if total > 0 else 0

    return render(request, 'home/designer_dashboard.html', {
        'total_tasks': total,
        'sent_tasks': sent,
        'published_tasks': published,
        'in_progress_tasks': in_progress,         # QuerySet
        'in_progress_count': in_progress.count(), # العدد
        'completed_tasks': completed,
        'pending_tasks': pending,
        'progress_percent': progress_percent,
    })

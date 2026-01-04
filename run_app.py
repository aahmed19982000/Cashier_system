import webview
import threading
from waitress import serve
import os
import time

# إعدادات دجانجو
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")  # تأكد من اسم مشروعك
import django
django.setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

def start_server():
    # تشغيل السيرفر
    serve(application, host='127.0.0.1', port=8000)

def load_logic(window):
    """
    هذه الوظيفة تعمل بمجرد فتح النافذة، تنتظر السيرفر ثم تغير الرابط
    """
    # انتظر قليلاً لضمان تشغيل السيرفر (مثلاً 3 ثوانٍ)
    time.sleep(10) 
    # تغيير رابط النافذة من شاشة التحميل إلى نظام الـ POS
    window.load_url("http://127.0.0.1:8000/pos")

if __name__ == "__main__":
    # 1. تشغيل السيرفر في الخلفية
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    # 2. إنشاء محتوى شاشة التحميل (HTML بسيط داخل الكود)
    splash_html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <style>
            body { 
                background: #2c3e50; color: white; 
                display: flex; flex-direction: column; 
                justify-content: center; align-items: center; 
                height: 100vh; margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .loader {
                border: 5px solid #f3f3f3; border-top: 5px solid #3498db;
                border-radius: 50%; width: 50px; height: 50px;
                animation: spin 1s linear infinite; margin-bottom: 20px;
            }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            h2 { margin-bottom: 5px; }
            p { color: #bdc3c7; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="loader"></div>
        <h2> جاري تشغيل نظام ادارة المطعم خلال 10 ثواني POS...</h2>
        <p>تم التطوير بواسطة: احمد ابراهيم 01099437596</p>
    </body>
    </html>
    """

    # 3. إنشاء النافذة وعرض شاشة التحميل أولاً
    window = webview.create_window(
        "نظام الكاشير الاحترافي", 
        html=splash_html, 
        width=1200, 
        height=800,
        resizable=True
    )

    # 4. تشغيل المنطق الذي سينتظر السيرفر ثم يحول الصفحة
    webview.start(load_logic, window)
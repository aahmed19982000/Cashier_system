@echo off
REM انتقل لمجلد المشروع
cd /d D:\Cashier_system

REM شغّل البيئة الافتراضية
call venv\Scripts\activate

REM شغّل سيرفر Django على العنوان 127.0.0.1:8000
start "" python manage.py runserver 127.0.0.1:8000

REM افتح المتصفح تلقائيًا على رابط المشروع
start http://127.0.0.1:8000

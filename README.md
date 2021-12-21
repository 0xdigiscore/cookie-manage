# 项目说明

Python版本需求：3.6及以上版本

项目环境搭建：python install -r requirements.txt

项目启动：python manage.py runserver 0.0.0.0:8000

工作进程启动：celery -A cookiemanage worker -l info

定时进程启动：celery -A cookiemanage beat -l info

远程脚本程序：
1. python half_auto_active_cookie.py
2. python half_auto_help_power.py

"""cookiemanage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cookie.remote_api import get_account_info, post_account_cookie_info
from cookie.remote_api import get_account_cookie_active_info, post_account_cookie_active_info

urlpatterns = [
    path('admin/', admin.site.urls),

    path('remote/api/get_account_info/',get_account_info),
    path('remote/api/post_account_cookie_info/',post_account_cookie_info),


    path('remote/api/get_account_cookie_active_info/',get_account_cookie_active_info),
    path('remote/api/post_account_cookie_active_info/',post_account_cookie_active_info),
]

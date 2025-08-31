"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from lib.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('login',login_user,name="login_details"),
    path('signup',student_signup,name="studentsignup"),
    path('book_details',book_details,name = "bookdetails"),
    path('admin_dashboard',admin_login,name='admin_login'),
    path('student_dashboard',student_login,name='student_login'),
    path('add_book',book_add,name='addbook'),
    path('updatebook/<pk>/',updatebook,name='updatebook'),
    path('deletebook/<pk>',deletebook,name='deletebook'),
    path('take_book',take_book,name = 'takebook'),
    path('takebook/<pk>',takebook,name='takebook'),
    path('retainbook/<pk>',retainbook,name = 'retainbook' ),
    path('logout',logout_user,name='log_out'),
    path('siva',tracker_view, name='tracker_view'),          # Main map page
    path('save_gps/', save_gps, name='save_gps'), 

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

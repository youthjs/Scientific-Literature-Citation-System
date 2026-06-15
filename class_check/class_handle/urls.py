# -*- coding: utf-8 -*-
# FileName  : urls.py

from django.urls import path
from . import views


app_name = 'class_handle'
urlpatterns = [
    path('', views.index, name='index'),
    path('check/', views.check, name='check'),
    path('news_check/', views.news_check, name='news_check'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('show/', views.show, name='show'),
]

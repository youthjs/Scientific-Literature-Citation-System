from django.contrib import admin
from .models import ClassCheckModel, UserInfoModel, myModel
from django.urls import path
from django.template.response import TemplateResponse




class ClassCheckAdmin(admin.ModelAdmin):
    list_display = ('news_text', 'check_result', 'check_time')


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')


admin.site.register(ClassCheckModel, ClassCheckAdmin)
admin.site.register(UserInfoModel, UserInfoAdmin)
admin.site.site_header = '科技文献关联关系分类系统'

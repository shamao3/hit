"""untitled10 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from .staticView import myResource,roomclass,manage,adddel,index,borrowableTable,fillTable,login,add,dell,cancel_reserver,detail,notice,personal_center,myApplication
urlpatterns = [
    url(r'^$',index),
    url(r'^index$',index),
    url(r'^myresource$',myResource),#资源管理
    url(r'^roomclass$', roomclass),#查询可借资源的选择分类
    url(r'^manage$', manage),#个人中心
    url(r'^adddel$', adddel),#人事管理
    url(r'^add$', add),#添加账户
    url(r'^dell$', dell),#删除账户
    url(r'^borrowable$', borrowableTable), #预约填表
    url(r'^filltable$', fillTable),
    url(r'^login$', login),#登录
    url(r'^cancel$', cancel_reserver),#取消预约
    url(r'^detail$', detail),#预约详情
    url(r'^notice$', notice),#通知主页面
    url(r'^personal_center$', personal_center),#个人中心主页面
    url(r'^my_application$', myApplication),#我的申请
]

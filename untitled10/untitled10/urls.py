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
from .staticView import myResource,roomclass,manage,adddel,index,borrowableTable,fillTable,login,add,dell,cancel_reserver,detail,notice,myApplication,personal_information,my_resource,else_notice
from .formAction import del_user,get_booking_table,add_user
from .dericLeung import login_check，getavailableres
from .zxl import cancel_detail

urlpatterns = [
    url(r'^$',index),
    url(r'^index$',index),
    url(r'^myresource$',myResource),#资源管理
    url(r'^roomclass$', roomclass),#查询可借资源的选择分类
    url(r'^manage$', manage),#个人中心
    url(r'^adddel$', adddel),#人事管理
    url(r'^add$', add),#添加账户 post，迟点在做
    url(r'^dell$', dell),#删除账户

    url(r'^filltable$', fillTable),#预约填表
    url(r'^login$', login),#登录
    url(r'^cancel$', cancel_reserver),#取消预约
    url(r'^detail$', detail),#预约详情
    url(r'^notice$', notice),#通知主页面
    url(r'^my_application$', myApplication),#我的申请
    url(r'^personal_information$', personal_information),#信息查看
    url(r'^my_resource$', my_resource),#通知界面中我的资源
    url(r'^else_notice$',else_notice ),#通知界面中其他资源

    #POST
    url(r'^login_check$', login_check),
    url(r'^del_user$', del_user),
    url(r'^get_booking_table$',get_booking_table),#booking_table界面中POST
    url(r'^add_user$',add_user),#添加账户POST
    #url(r'^get_resManagement_Info$', get_resManagement_Info),#资源管理POST 错了，没写完

    #GET
    url(r'^borrowable/$', getavailableres),#可预约资源
    url(r'^cancel$', cancel_detail),#取消预约
]

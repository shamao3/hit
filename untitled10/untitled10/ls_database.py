from django.db import connection,models
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils import timezone

import datetime

from datetime import date


def registered(request):
    from django.db import connection, transaction
    if request.method == 'POST':
        username = request.POST.get("userName")
        name = request.POST.get("name")
        password = request.POST.get("password")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")

    cursor = connection.cursor()
    cursor.execute(
        'Insert into userModel_user(name,userName,password,privilige,startdate,enddate) values(@a,"2","2","2","2","2") ')
        # names = [row[0] for row in cursor.fetchall()]
    connection.close
    return HttpResponse("添加成功！")

def delete(requset):
    if requset.method == 'POST':
        user = requset.POST.get("usercode")

    cursor = connection.cursor()
    cursor.execute('delete from userModel_user where userName = 2')
    connection.close
    return HttpResponse("注销成功！")
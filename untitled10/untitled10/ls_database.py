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
        userid = request.session.get('userid', '')
    cursor = connection.cursor()
    cursor.execute(
        'Insert into userModel_user (name,userName,password,privilige,startdate,enddate)'        
        #'values( "'+username+' + '+name+' + '+password+' + 1 + '+startDate+' + '+endDate+'")')
         'values( "'+str(username)+'" , "'+str(name)+'" , "'+str(password)+'" , "student" , "'+str(startDate)+'" , "'+str(endDate)+'")'
         'Insert into userModel_userrelationship (childuser_id,upperuser_id)' 'values()'
        )

    connection.close
    return HttpResponse("添加成功！")
    # return HttpResponse("userName:" + username + ";name:" + name + ";password:" + password + ";startDate:"
    #               + startDate + ";endDate:" + endDate) (name,userName,password,privilige,startdate,enddate)

def delete(request):
    request.session.clear_expired()
    if request.method == 'POST':
        cancell = request.POST.get("usercode")
        userid = request.session.get('userid', '')
    # cursor = connection.cursor()
    # cursor.execute('delete  from userModel_user a, userModel_userrelationship b,'
    #                'userModel_user c where ' 'a.id = b.upperuser_id and b.childuser_id = c.id and c.userName = "'+cancell+'"')
    # connection.close
    with connection.cursor() as cursor:
        sql = 'SELECT c.userName FROM userModel_user a, userModel_userrelationship b,userModel_user c WHERE ' \
            'a.id = b.upperuser_id and b.childuser_id = c.id and c.userName = "'+cancell+'"'
        cursor.execute(sql)
        result = cursor.fetchall
    if(result != ''):
        cursor = connection.cursor()
        cursor.execute('delete  from userModel_user where id = "'+userid+'"')
        connection.close
        return HttpResponse("注销成功！")
    else:
        return HttpResponse("注销失败！")
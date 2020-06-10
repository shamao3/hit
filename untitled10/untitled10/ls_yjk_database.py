from django.db import connection,models
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils import timezone

import datetime

from datetime import date


def add_Child(request):
    from django.db import connection, transaction
    if request.method == 'POST':
        username = request.POST.get("userName")
        name = request.POST.get("name")
        password = request.POST.get("password")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")
        userid = request.session.get('userid', '')
    sql = 'SELECT id FROM userModel_user WHERE userName="{}";'
    sql = sql.format(name)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        if (len(result) != 0):
            return render(request, "./person_add.html", {"text2": "存在同名用户，无法添加"})
        else:
            sql = 'Insert into userModel_user (name,userName,password,privilige,startdate,enddate) values( "' + str(
                username) + '" , "' + str(name) + '" , "' + str(password) + '" , "student" , "' + str(
                startDate) + '" , "' + str(endDate) + '");'
            with connection.cursor() as cursor:
                cursor.execute(sql)
                sql = 'SELECT id FROM userModel_user WHERE userName="{}";'
                sql = sql.format(name)
                cursor.execute(sql)
                result = cursor.fetchall()
                if (len(result) != 0):
                    ch_id = result[0][0]
                    sql = 'Insert into userModel_userrelationship (childuser_id,upperuser_id) values( "' + str(
                        ch_id) + '" , "' + str(userid) + '");'
                    cursor.execute(sql)
                    return render(request, "./person_adddel.html", {"text": "添加成功！"})

                else:
                    return render(request, "./person_add.html", {"text2": "添加失败！"})







    # cursor = connection.cursor()
    # cursor.execute(
    #     'Insert into userModel_user (name,userName,password,privilige,startdate,enddate)'
    #     #'values( "'+username+' + '+name+' + '+password+' + 1 + '+startDate+' + '+endDate+'")')
    #      'values( "'+str(username)+'" , "'+str(name)+'" , "'+str(password)+'" , "student" , "'+str(startDate)+'" , "'+str(endDate)+'")'
    #      'Insert into userModel_userrelationship (childuser_id,upperuser_id)' 'values()'
    #     )
    #
    # connection.close
    # return HttpResponse("添加成功！")
    # return HttpResponse("userName:" + username + ";name:" + name + ";password:" + password + ";startDate:"
    #               + startDate + ";endDate:" + endDate) (name,userName,password,privilige,startdate,enddate)

def delete_user(request):
    request.session.clear_expired()
    if request.method == 'POST':
        del_userName = request.POST.get("delete_user")
        userid = request.session.get('userid', '')
    else:
        return HttpResponse("!!!")
    # cursor = connection.cursor()
    # cursor.execute('delete  from userModel_user a, userModel_userrelationship b,'
    #                'userModel_user c where ' 'a.id = b.upperuser_id and b.childuser_id = c.id and c.userName = "'+cancell+'"')
    # connection.close
    sql = 'SELECT id FROM userModel_user WHERE userName="{}";'
    sql = sql.format(del_userName)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        if (len(result) != 0):
            del_userID = result[0][0]
            up_id = del_userID
        else:
            return HttpResponse("该用户不存在")
    a = 0

    while len(result) != 0:
        sql = 'SELECT upperuser_id FROM userModel_userrelationship WHERE childuser_id={};'
        sql = sql.format(up_id)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            if (len(result) != 0):
                up_id = result[0][0]
                if (userid == up_id):
                    a = 1
                    break
            else:
                return HttpResponse("您没有权限注销该用户")
    sql = 'DELETE from userModel_record where user_id={};'
    sql = sql.format(del_userID)
    with connection.cursor() as cursor:
        cursor.execute(sql)
    sql = 'DELETE from userModel_resourcebelonging where owner_id={};'
    sql = sql.format(del_userID)
    with connection.cursor() as cursor:
        cursor.execute(sql)
    sql = 'SELECT upperuser_id FROM userModel_userrelationship WHERE childuser_id={};'
    sql = sql.format(del_userID)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        if (len(result) != 0):
            up_id = result[0][0]
    sql = 'DELETE from userModel_userrelationship where childuser_id={};'
    sql = sql.format(del_userID)
    with connection.cursor() as cursor:
        cursor.execute(sql)
    sql = 'UPDATE userModel_userrelationship SET upperuser_id ={} WHERE upperuser_id = {};'
    sql = sql.format(up_id, del_userID)
    with connection.cursor() as cursor:
        cursor.execute(sql)
    sql = 'DELETE from userModel_user WHERE id={};'
    sql = sql.format(del_userID)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return render(request,"./person_adddel.html",{"text":"删除成功！"})






    # with connection.cursor() as cursor:
    #     sql = 'SELECT c.userName FROM userModel_user a, userModel_userrelationship b,userModel_user c WHERE ' \
    #         'a.id = b.upperuser_id and b.childuser_id = c.id and c.userName = "'+cancell+'"'
    #     cursor.execute(sql)
    #     result = cursor.fetchall
    # if(result != ''):
    #     cursor = connection.cursor()
    #     cursor.execute('delete  from userModel_user where id = "'+userid+'"')
    #     connection.close
    #     return HttpResponse("注销成功！")
    # else:
    #     return HttpResponse("注销失败！")
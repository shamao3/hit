from datetime import date
from django.db import connection, models
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .dericLeung import checksession


def else_get(request):
    username = checksession(request)
    if username == False:
        return redirect('/login')
    a = request.session.get('userid', '')
    print(a)
    with connection.cursor() as cursor:
        sql = 'SELECT b.text,b.isread from userModel_othernotice b,userModel_record a where a.user_id=' + str(a)
        cursor.execute(sql)
        result = cursor.fetchall()
        res = []
        dic = {}
        i = 1
        if (len(result) != 0):
            for notice in result:
                dic['num'] = i
                dic['text'] = notice[0]
                dic['isread'] = notice[1]
                res.append(dic.copy())  # res中的数据也发生变化主要原因是dict是一个可变的对象，list在append的时候，只是append了对象的引用，没有append对象的数据。
                # 修改了对象之后，之前append过的对象也会发生变化。改进：使用copy
                i += 1
                print(res)
            return render(request, './else_notice.html', {"notice": res})
        else:
            return HttpResponse("Error")

def my_res(request):
    a=request.session.get('userid', '')
    print(a)

    with connection.cursor() as cursor:
        sql='SELECT a.extras,a.startdate,b.location,c.userName from userModel_resource b,userModel_record a,userModel_user c ' \
            'where b.id=a.resource_id and a.user_id=c.id and a.user_id='+str(a)
        cursor.execute(sql)
        result = cursor.fetchall()
        res=[]
        dic={}
        i=1
        if(len(result)!=0):
            for my_res in result:
                dic['num']=i
                dic['date']=my_res[0]
                dic['location']=my_res[1]
                dic['extras'] = my_res[2]
                dic['userName'] = my_res[3]
                res.append(dic.copy())#res中的数据也发生变化主要原因是dict是一个可变的对象，list在append的时候，只是append了对象的引用，没有append对象的数据。
                # 修改了对象之后，之前append过的对象也会发生变化。改进：使用copy
                i+=1
                print(res)
            return render(request,'./my_resource.html',{"my_res":res})
        else : return HttpResponse("Error")

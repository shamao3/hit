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
        sql = 'SELECT a.text,a.isread from userModel_othernotice a,userModel_record b where b.user_id=' + str(a)
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
        sql='SELECT b.extras,b.startdate,a.location c.userName' \
            'from userModel_resource a,userModel_record b,userModel_user c ' \
            'where a.id=b.resource_id and b.user_id=c.id and b.user_id='+str(a)
        cursor.execute(sql)
        result = cursor.fetchall()
        res=[]
        dic={}
        i=1
        if(len(result)!=0):
            for detail in result:
                dic['num']=i
                dic['date']=myres[0]
                dic['location']=myres[1]
                dic['extras'] = myres[2]
                dic['userName'] = myres[3]
                res.append(dic.copy())#res中的数据也发生变化主要原因是dict是一个可变的对象，list在append的时候，只是append了对象的引用，没有append对象的数据。
                # 修改了对象之后，之前append过的对象也会发生变化。改进：使用copy
                i+=1
                print(res)
            return render(request,'./my_resource.html',{"my_res":res})
        else : return HttpResponse("Error")

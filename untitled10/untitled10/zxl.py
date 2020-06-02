from django.db import connection,models
from django.http import HttpResponse
from django.shortcuts import render,redirect
from datetime import date


def cancel_detail(request):
    a=request.session.get('userid', '')
    print(a)
    with connection.cursor() as cursor:
        sql='SELECT name,state from userModel_resource a,userModel_record b where a.id=b.resource_id and b.user_id ='+str(a)
        cursor.execute(sql)
        result = cursor.fetchall()
        res=[]
        dic={}
        i=1
        if(len(result)!=0):
            for detail in result:
                dic['num']=i
                dic['name']=detail[0]
                dic['state']=detail[1]
                res.append(dic.copy())#res中的数据也发生变化主要原因是dict是一个可变的对象，list在append的时候，只是append了对象的引用，没有append对象的数据。
                # 修改了对象之后，之前append过的对象也会发生变化。改进：使用copy
                i+=1
                print(res)
            return render(request,'./cancel_reserve.html',{"detail":res})
        else : return HttpResponse("no")

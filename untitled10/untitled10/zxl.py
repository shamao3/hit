from django.db import connection,models
from django.http import HttpResponse
from django.shortcuts import render,redirect
from datetime import date

from .dericLeung import checksession



def detail(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')
    #a = request.session.get('userid', '')
    id = request.GET.get('id','')
    dic={}
    with connection.cursor() as cursor:
        #sql = 'SELECT b.state userModel_resource a userModel_record b where b.id='+str(a)+' and a.name="'+name+'"and a.id=b.resource_id'
        sql='SELECT a.state from userModel_record a where id ='+str(id)
        cursor.execute(sql)
        result=cursor.fetchall()
        for i in result:
            dic['state']=i[0]
            dic['username']=username
        return render(request,'./detail.html',dic)
def getmyRes(page='1',id=None):#分页函数
    if (id == None):
        return []
    else:
        with connection.cursor() as cursor:#读取数据

            sql = 'SELECT a.name,b.state,b.id from userModel_resource a,userModel_record b where a.id=b.resource_id ' \
                  'and (b.state="预约成功" or b.state="处理中") and b.user_id ='+id
            cursor.execute(sql)
            result = cursor.fetchall()
            res = []
            dic = {}
            i = 1
            if (len(result) != 0):
                for detail in result:
                    dic['num'] = i
                    dic['name'] = detail[0]
                    dic['state'] = detail[1]
                    dic['id']=detail[2]
                    res.append(dic.copy())  # res中的数据也发生变化主要原因是dict是一个可变的对象，list在append的时候，只是append了对象的引用，没有append对象的数据。
                    # 修改了对象之后，之前append过的对象也会发生变化。改进：使用copy
                    i += 1
                    print(res)
            size=len(result)//7+1#得到数据量
            pages={}
            for i in range(0,size):
                beginindex = 7 * i#一页中的开始
                endindex = 7 * (i + 1)#一页中的结束
                if (endindex > len(res)):#若超出数据量则将最后的数据作为一页的最后
                    endindex = len(res)
                tempgroup = res[beginindex:endindex]#将第i+1的数据装入tempgroup
                pages[str(i + 1)] = tempgroup#将temp装入字典  key为i+1
            return pages.get(page, '1'), range(1, size + 1)#返回key为page的value和总页面数量数组
        return []
def cancel_detail(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')
    page = request.GET.get('page', '1')
    a = str(request.session.get('userid', ''))
    result, size = getmyRes(page=page, id=a)#页面数据和总页面数量列表
    return render(request, './cancel_reserve.html', {'username': username, 'size': size, 'resource': result})
def delete(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')
    id=request.GET.get('id','')
    sql='DELETE from userModel_record where id='+str(id)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return redirect('/cancel')
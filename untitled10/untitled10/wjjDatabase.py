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
    page = request.GET.get('page', '1')
    print(a)
    print(page)
    result,size = getOther(page=page,id=a)
    return render(request, './else_notice.html', {'size': size, 'notice': result})


def my_res(request):
    username = checksession(request)
    if username == False:
        return redirect('/login')
    a=request.session.get('userid', '')
    print(a)
    page = request.GET.get('page', '1')
    result, size = getres(page=page, id=a)
    return render(request, './my_resource.html', {'size': size, 'my_res': result})


def judgeAgree(request):
    print(1)
    username = checksession(request)
    if (username == False):
        return redirect('/login')
    isAgree=request.GET.get('agree','')#获取参数
    location=request.GET.get('name','')
    num=request.GET.get('num','')
    page = int(num)//7+1
    sql = ''
       # sqlread = 'select id,isavailable from userModel_resource a ,userModel_record b where b.resource_id'
    with connection.cursor() as cursor:
       sql = 'SELECT id from userModel_resource where name = "'+ str(location) + '"'
       print(2)
       cursor.execute(sql)
       result = cursor.fetchall()
       print(result)
       if(isAgree == "True"):
            state = "预约成功"
       else:
             state = "预约失败"
       print(state)
       if (len(result) != 0):
           sql = 'update userModel_record  set state = "' + str(state) + '" where resource_id = ' + str(result[0][0])
           cursor.execute(sql)
           cursor.close()
    return redirect('/my_resource/?page='+str(page))

def haveRead(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')
    isRead = request.GET.get('read', '')  # 获取参数
    idofnotice = request.GET.get('id', '')
    num = request.GET.get('num','')
    page = int(num)//7+1
    sql = ''
    with connection.cursor() as cursor:
           if(isRead == "False"):
                sql = 'update userModel_othernotice  set isread = "True" where id = '+idofnotice
           cursor.execute(sql)
           cursor.close()
    return redirect('/else_notice/?page='+str(page))

def getOther(page='1',id=None):
    if (id == None):
        return []
    else:
        with connection.cursor() as cursor:
            sql = 'SELECT text,isread,id from userModel_othernotice where user_id = ' + str(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            size = (len(result) - 1) // 7 + 1
            res = []
            dic = {}
            i = 1
            if (len(result) != 0):
                for notice in result:
                    dic['num'] = i
                    dic['text'] = notice[0]
                    dic['is_read'] = str(notice[1])
                    dic['id'] = notice[2]
                    res.append(dic.copy())  # res中的数据也发生变化主要原因是dict是一个可变的对象，list在append的时候，只是append了对象的引用，没有append对象的数据。
                    # 修改了对象之后，之前append过的对象也会发生变化。改进：使用copy
                    i += 1
                    print(res)
            else:
                return [], range(1, 2)
            size = (len(result) - 1) // 7 + 1  # 得到数据量
            pages = {}
            for i in range(0, size):
                beginindex = 7 * i  # 一页中的开始
                endindex = 7 * (i + 1)  # 一页中的结束
                if (endindex > len(res)):  # 若超出数据量则将最后的数据作为一页的最后
                    endindex = len(res)
                tempgroup = res[beginindex:endindex]  # 将第i+1的数据装入tempgroup
                pages[str(i + 1)] = tempgroup  # 将temp装入字典  key为i+1
                print(page)
            return pages.get(page, '1'), range(1, size + 1)  # 返回key为page的value和总页面数量数组
        return []

def getres(page='1',id=None):
    if (id == None):
        return []
    else:
        with connection.cursor() as cursor:
            sql = 'SELECT a.extras,a.startdate,b.name,c.userName from userModel_resource b,userModel_record a,userModel_user c ' \
                  'where b.id=a.resource_id and a.state="处理中" and a.user_id=c.id and a.user_id=' + str(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            size = (len(result) - 1) // 7 + 1
            res = []
            dic = {}
            i = 1
            if (len(result) != 0):
                for my_res in result:
                    dic['num'] = i
                    dic['extras'] = my_res[0]
                    dic['date'] = my_res[1]
                    dic['location_name'] = my_res[2]
                    dic['userName'] = my_res[3]
                    res.append(dic.copy())  # res中的数据也发生变化主要原因是dict是一个可变的对象，list在append的时候，只是append了对象的引用，没有append对象的数据。
                    # 修改了对象之后，之前append过的对象也会发生变化。改进：使用copy
                    i += 1
                    print(res)
            else:
                return [],range(1, 2)
            size = (len(result) - 1) // 7 + 1  # 得到数据量
            pages = {}
            for i in range(0, size):
                beginindex = 7 * i  # 一页中的开始
                endindex = 7 * (i + 1)  # 一页中的结束
                if (endindex > len(res)):  # 若超出数据量则将最后的数据作为一页的最后
                    endindex = len(res)
                tempgroup = res[beginindex:endindex]  # 将第i+1的数据装入tempgroup
                pages[str(i + 1)] = tempgroup  # 将temp装入字典  key为i+1
                print(page)
            return pages.get(page, '1'), range(1, size + 1)  # 返回key为page的value和总页面数量数组

        return []
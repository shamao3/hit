from datetime import date
from django.db import connection, models
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .dericLeung import checksession


def getMyApp(page='1',id=None):
    if (id == None):
        return []
    else:

        with connection.cursor() as cursor:
            sql='SELECT b.name,a.startdate,a.extras,a.id FROM userModel_record a,userModel_resource b WHERE ' \
            'a.resource_id=b.id and a.user_id='+id
        # sql='SELECT * FROM userModel_user where id='+str(a)
            cursor.execute(sql)
            result = cursor.fetchall()
            res=[]
            num=1
            if(len(result)!=0):
                for j in result:
                    temp = {}
                    temp['num'] = num
                    temp['date'] = j[1]
                    temp['resource'] = j[0]
                    temp['content'] = j[2]
                    temp['id']=j[3]
                    res.append(temp.copy())
                    num+=1
                    print(res)
            size=(len(result)-1)//7+1
            pages = {}
            for i in range(0, size):
                beginindex = 7 * i  # 一页中的开始
                endindex = 7 * (i + 1)  # 一页中的结束
                if (endindex > len(res)):  # 若超出数据量则将最后的数据作为一页的最后
                    endindex = len(res)
                tempgroup = res[beginindex:endindex]  # 将第i+1的数据装入tempgroup
                pages[str(i + 1)] = tempgroup  # 将temp装入字典  key为i+1
            return pages.get(page, '1'), range(1, size + 1)  # 返回key为page的value和总页面数量数组
        return []
def getMyApplication(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')
    page = request.GET.get('page', '1')
    a = str(request.session.get('userid', ''))
    result, size = getMyApp(page=page, id=a)
    return render(request, './my_application.html', {'username': username, 'size': size, 'applicationData': result,'page':page})
def getPersonalInformation(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')
    a = request.session.get('userid', '')
    print (a)
    with connection.cursor() as cursor:

        if(str(a)=='1'):


            sql0='SELECT username,startdate,enddate,privilige FROM userModel_user WHERE id="1"'
            cursor.execute(sql0)
            result0=cursor.fetchall()
            temp0 = {}
            temp0['accountName'] = result0[0][0]
            temp0['startdate'] = result0[0][1].strftime('%Y-%m-%d')
            temp0['enddate'] = result0[0][2].strftime('%Y-%m-%d')
            temp0['upperuser'] = "nobody"
            temp0['privilige'] = result0[0][3]
            return render(request, "personal_information.html", temp0)

        else:

            sql='SELECT a.userName,a.startdate,a.enddate,b.userName,a.privilige FROM userModel_user a,userModel_user b,' \
                'userModel_userrelationship c WHERE c.childuser_id=a.id and c.upperuser_id=b.id and a.id='+str(a)
            #sql='SELECT * FROM userModel_user where id="'+id+'"'
            cursor.execute(sql)
            result = cursor.fetchall()
            temp = {}
            print(result)
            if (len(result) != 0):
                temp['accountName'] = result[0][0]
                temp['startdate'] = result[0][1].strftime('%Y-%m-%d')
                temp['enddate'] = result[0][2].strftime('%Y-%m-%d')
                temp['upperuser'] = result[0][3]
                temp['privilige']=result[0][4]
                return render(request,"./personal_information.html",temp)
            else:
                return HttpResponse("Error")

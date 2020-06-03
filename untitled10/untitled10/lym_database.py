from datetime import date
from django.db import connection, models
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .dericLeung import checksession


def getMyApplication(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')
    a=request.session.get('userid', '')
    print (a)
    with connection.cursor() as cursor:
        sql='SELECT b.name,a.startdate,a.extras FROM userModel_record a,userModel_resource b WHERE ' \
            'a.resource_id=b.id and a.user_id='+str(a)
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
                res.append(temp.copy())
                num+=1
            return render(request,'./my_application.html',{'applicationData':res})
        else :
            return HttpResponse("ERROR")


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
            if (len(result) != 0):
                temp['accountName'] = result[0][0]
                temp['startdate'] = result[0][1].strftime('%Y-%m-%d')
                temp['enddate'] = result[0][2].strftime('%Y-%m-%d')
                temp['upperuser'] = result[0][3]
                temp['privilige']=result[0][4]
                return render(request,"./personal_information.html",temp)
            else:
                return HttpResponse("Error")
from datetime import date
from django.db import connection, models
from django.http import HttpResponse
from django.shortcuts import render, redirect


def getMyApplication(request):
    a=request.session.get('userid', '')
    print (a)
    with connection.cursor() as cursor:
        sql='SELECT b.name,a.startdate,a.extras FROM userModel_record a,userModel_resource b WHERE ' \
            'a.resource_id=b.id and a.user_id='+str(a)
        # sql='SELECT * FROM userModel_user where id='+str(a)
        cursor.execute(sql)
        result = cursor.fetchall()
        res=[]
        temp={}
        num=1
        if(len(result)!=0):
            for j in result:
                temp['num'] = num
                temp['date'] = j[1]
                temp['resource'] = j[0]
                temp['content'] = j[2]
                res.append(temp.copy())
                num+=1
            return render(request,'./my_application.html',{'applicationData':res})
        else : return HttpResponse("ERROR")
def getPersonalInformation(request):
    a = request.session.get('userid', '')
    print (a)
    with connection.cursor() as cursor:

     if(str(a)=='1'):


         sql0='SELECT username,startdate,enddate,privilige FROM userModel_user WHERE id="1"'
         cursor.execute(sql0)
         result0=cursor.fetchall()
         res0=[]
         temp0={}
         for i in result0:
            temp0['accountName'] = i[0]
            temp0['startdate'] = i[1].strftime('%Y-%m-%d')
            temp0['enddate'] = i[2].strftime('%Y-%m-%d')
            temp0['upperuser'] = "nobody"
            temp0['privilige'] = i[3]
            res0.append(temp0.copy())
            return render(request, "personal_information.html", {"PerInfoData": res0})

     else:

           sql='SELECT a.userName,a.startdate,a.enddate,b.userName,a.privilige FROM userModel_user a,userModel_user b,' \
            'userModel_userrelationship c WHERE a.id='+str(a)+' and c.childuser_id=a.id and c.upperuser_id=b.id'
        #sql='SELECT * FROM userModel_user where id="'+id+'"'
           cursor.execute(sql)
           result = cursor.fetchall()
           res = []
           temp = {}
           if (len(result) != 0):
             for i in result:
                temp['accountName'] = i[0]
                temp['startdate'] = i[1].strftime('%Y-%m-%d')
                temp['enddate'] = i[2].strftime('%Y-%m-%d')
                temp['upperuser'] = i[3]
                temp['privilige']=i[4]
                res.append(temp.copy())
                return render(request,"personal_information.html",{"PerInfoData":res})
           else: return HttpResponse("Error")
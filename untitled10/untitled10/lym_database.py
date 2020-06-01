from django.db import connection,models
from django.http import HttpResponse
from datatime import date
def getMyApplication(requset):
    with connection.cursor() as cursor:
        sql1 = "SELECT a.id,b.name,a.starttime,a.extras  FROM userModel_record a,userModel_resource b WHERE a.resource_id=b.id"
        cursor.execute(sql1)
        result = cursor.fetchall()
        res=""
        for MyApplicationRes in result:
            res += MyApplicationRes[0] + " " + MyApplicationRes[1]+" "+MyApplicationRes[3]+" "+MyApplicationRes[4]
        return HttpResponse(res)
    return HttpResponse("ERROR")
def getPersonalInformation(request):
    with connection.cursor() as cursor:
        sql2="SELECT a.*,a.userName FROM userModel_user a,main.userModel_userrelationship b where a.id=b.childuser_id and b.upperuser_id=a.id"
        cursor.execute(sql2)
        result = cursor.fetchall()
        for userInfo in result:
            res += userInfo[1] + " " + userInfo[4]+" "+userInfo[5]

from django.http import HttpResponse
from django.db import connection,models

def login_check(request):
    if(request.method=='POST'):
        username=request.POST.get("username")
        pwd=request.POST.get("pwd")
        return HttpResponse("username : "+username+" ; pwd : "+ pwd)

def del_user(request):
    if(request.method=='POST'):
        usercode=request.POST.get("usercode")

        return HttpResponse("usercode : "+ usercode)
def add_user(request):
    if(request.method=='POST'):
        username = request.POST.get("userName")
        name = request.POST.get("name")
        password = request.POST.get("password")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")
        cursor = connection.cursor()
        cursor.execute(
            'Insert into userModel_user(name,userName,password,privilige,startdate,enddate) values("username","name","password","privilige","startDate","endDate") ')
        names = [row[0] for row in cursor.fetchall()]
        connection.close
        return HttpResponse("添加成功！")
        # return HttpResponse("userName:" + username + ";name:" + name + ";password:" + password + ";startDate:"
        #                     + startDate + ";endDate:" + endDate)
def get_booking_table(request):
    if(request.method=="POST"):
        roomname=request.POST.get("roomname")
        beginDate=request.POST.get("beginDate")
        beginTime=request.POST.get("beginTime")
        endDate=request.POST.get("endDate")
        endTime=request.POST.get("endTime")
        extras=request.POST.get("extras")
        return HttpResponse(
            "roomname:" + roomname + ";beginDate:" + beginDate + ";beginTime:" +
            beginTime + ";endDate:" + endDate + ";endTime:" + endTime+
            ";extras:" + extras)


from django.db import connection,models
from django.http import HttpResponse
from django.shortcuts import render,redirect
from datetime import date


def checksession(request):
    request.session.clear_expired()
    id=request.session.get('userid','')
    if(id):
        #更新时间
        request.session.set_expiry(120)
        return request.session.get('username','')
    else:
        return False







def login_check(request):
    request.session.clear_expired()
    username = ""
    pwd = ""
    if(request.method=='POST'):
        username=request.POST.get('username')
        pwd=request.POST.get('pwd')
    with connection.cursor() as cursor:

        sql = 'SELECT id,username,password,name FROM userModel_user WHERE username = "'+username+'"'
        cursor.execute(sql)
        result = cursor.fetchall()
        res = ""
        if(len(result)!=0):
            if(pwd == result[0][2]):
                #登陆成功，存入session
                request.session['userid']=result[0][0]
                name=result[0][3]
                request.session['username']=name
                request.session.set_expiry(120)
                response=render(request,"./index.html", {'username':name})
                response.set_cookie('username',name,604800)
                return response
            else:
                return render(request, "./login.html")
    return HttpResponse("ERROR")


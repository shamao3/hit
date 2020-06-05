from django.db import connection,models
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils import timezone
from datetime import date,datetime


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

def getavailableres(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')
    type = request.GET.get('type', '')
    page = request.GET.get('page','1')
    id = request.session.get('id','')
    place=''
    time=''
    result,size = getAvaRes(type=type,page=page)

    return render(request,'./resource_borrowable.html',{'resource':result,'username':username,'type':type,'size':size})


def getdate(request):
    with connection.cursor() as cursor:
        sql = 'SELECT startdate FROM userModel_record WHERE date('')'
        cursor.execute(sql)
        result = cursor.fetchall()
        res = ''
        return HttpResponse(result)


def searchres(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')
    if(request.method=='POST'):
        query=request.POST.get('query','')
        type=request.GET.get('type','')
        page = request.GET.get('page', '1')
        if(query==''):
            url = "/borrowable/?type="+type
            return redirect(url)
        else:
            arr=query.split(" ")
            time = ''
            place = ''
            for item in arr:
                if(isDate(item)):
                    time=item
                else:
                    place=item
            result,size=getAvaRes(page=page,type=type,time=time,place=place)
            return render(request, './resource_borrowable.html', {'resource': result, 'username': username, 'type': type,'size':size})


def isDate(str):
    try:
        datetime.strptime(str,"%Y-%m-%d")
        return True
    except:
        return False

def getAvaRes(type,page,time='now',place=''):#两个都是string
    with connection.cursor() as cursor:
        sql=''
        if(place==''):
            sql = 'SELECT name FROM userModel_record a, userModel_resource b WHERE a.resource_id = b.id and b.type = "'+ type +'" and b.isavailable = "True"' \
                  'and b.id not in (SELECT resource_id FROM userModel_record where startdate <= date("'+time+'") and enddate>=date("'+time+'") and state = "预约成功")'
        else:
            sql= 'SELECT name FROM userModel_record a, userModel_resource b WHERE a.resource_id = b.id and b.type = "'+ type +'" and b.isavailable = "True"' \
                  'and b.id not in (SELECT resource_id FROM userModel_record where startdate <= date("'+time+'") and enddate>=date("'+time+'") and state = "预约成功") ' \
                'and b.location="'+place+'"'
        cursor.execute(sql)
        result = cursor.fetchall()
        res=[]
        for i in range(0,len(result)):
            tempdic={'id':i+1,'name':result[i][0]}
            res.append(tempdic)
        size = len(res)//7+1
        resdic={}
        for i in range(0,size):
            beginindex=i*7
            endindex=i*7+7
            if(endindex>len(res)-1):
                endindex=len(res)
            tempgroup=res[beginindex:endindex]
            resdic[str(i+1)]=tempgroup
        group=resdic.get(page,[])
        sizegroup=range(0,size)
        return  group,sizegroup
    return []

def resourcemanage(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')
    page=request.GET.get('page','1')
    id=str(request.session.get('userid',''))
    result,size = getmyres(page=page,id=id)

    return render(request,'./resource_management.html',{'username':username,'size':size,'resource':result,'page':page})

def getmyres(page='1',id=None):
    if(id==None):
        return []
    else:
        sql = 'select name,isavailable from userModel_resource a ,userModel_resourcebelonging b ' \
              'where a.id=b.resource_id and b.owner_id='+id
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            res=[]
            for index in range(0, len(result)):
                tempdic={'id':index+1, 'name':result[index][0]}
                if(result[index][1]=='True'):
                    tempdic['state']='可借用'
                else:
                    tempdic['state']='不可借用'
                res.append(tempdic)
            size = len(result)//7+1
            pages={}
            for i in range(0,size):
                beginindex=7*i
                endindex=7*(i+1)
                if(endindex>len(res)):
                    endindex=len(res)
                tempgroup=res[beginindex:endindex]
                pages[str(i+1)]=tempgroup
            return pages.get(page,'1'),range(1,size+1)
        return []

def reversestate(request):
    if(request.method=='POST'):
        changeitems=request.POST.getlist('shift',[])
        thispage=request.GET.get('page','')
        sqlread = 'select id,isavailable from userModel_resource'
        if(len(changeitems)!=0):
            sqlread+=' where id in ('
            for id in changeitems:
                sqlread+=' '+id+','
            sqlread=sqlread[:-1]+')'
            with connection.cursor() as cursor:
                cursor.execute(sqlread)
                result=cursor.fetchall()
                for item in result:
                    state=item[1]
                    print(state)
                    if(state=='False'):
                        state='True'
                    else:
                        state='False'
                    sql1 = 'update userModel_resource set isavailable= "'+str(state)+'" where id = '+ str(item[0])
                    cursor.execute(sql1)
                cursor.close()
        return redirect('/myresource/?page='+thispage)







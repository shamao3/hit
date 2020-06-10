from django.db import connection,models
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils import timezone
from datetime import date,datetime
from .formAction import get_booking_table


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
        type = request.GET.get('type','')
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
            sql = 'SELECT name FROM userModel_resource b WHERE b.type = "'+ type +'" and b.isavailable = "True"' \
                  'and b.id not in (SELECT resource_id FROM userModel_record where startdate <= date("'+time+'") and enddate>=date("'+time+'") and state = "预约成功")'
        else:
            sql= 'SELECT name FROM userModel_resource b WHERE b.type = "'+ type +'" and b.isavailable = "True"' \
                  'and b.id not in (SELECT resource_id FROM userModel_record where startdate <= date("'+time+'") and enddate>=date("'+time+'") and state = "预约成功") ' \
                'and b.location="'+place+'"'
        cursor.execute(sql)
        result = cursor.fetchall()
        res=[]
        for i in range(0,len(result)):
            tempdic={'id':i+1,'name':result[i][0]}
            res.append(tempdic)
        print(sql)
        size = (len(res)-1)//7+1
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

    isroot='false'
    if(id=='1'):
        isroot='true'
    result,size = getmyres(page=str(page),id=id)
    return render(request,'./resource_management.html',{'isroot':isroot,'username':username,'size':size,'resource':result,'page':page})

def othernotice(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')
    page=request.GET.get('page','1')
    id=str(request.session.get('userid',''))

    result,size = getmyres(page=str(page),id=id)
    return render(request,'./else_notice.html',{'username':username,'size':size,'resource':result,'page':page})


def my_res(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')
    page = request.GET.get('page', '1')
    id = str(request.session.get('userid', ''))

    result, size = getmyres(page=str(page), id=id)
    return render(request, './else_notice.html', {'username': username, 'size': size, 'resource': result, 'page': page})

def getmyres(page='1',id=None):
    if(id=='1'):
        sql = 'select name,isavailable,a.id from userModel_resource a ,userModel_resourcebelonging b ' \
              'where a.id=b.resource_id'

    else:
        sql = 'select name,isavailable,a.id from userModel_resource a ,userModel_resourcebelonging b ' \
              'where a.id=b.resource_id and b.owner_id='+id
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        res=[]
        for index in range(0, len(result)):
            tempdic={'id':index+1, 'name':result[index][0],'resid':result[index][2]}
            if(result[index][1]=='True'):
                tempdic['state']='可借用'
            else:
                tempdic['state']='不可借用'
            res.append(tempdic)
        size = (len(result)-1)//7+1
        pages={}
        for i in range(0,size):
            beginindex=7*i
            endindex=7*(i+1)
            if(endindex>len(res)):
                endindex=len(res)
            tempgroup=res[beginindex:endindex]
            pages[str(i+1)]=tempgroup
        return pages.get(page,[]),range(1,size+1)
    return []

def reversestate(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')
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
                    if(state=='False'):
                        state='True'
                    else:
                        state='False'
                    sql1 = 'update userModel_resource set isavailable= "'+str(state)+'" where id = '+ str(item[0])
                    cursor.execute(sql1)
                cursor.close()
        return redirect('/myresource/?page='+thispage)

def addrecord(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')
    dic=get_booking_table(request)
    resname = request.GET.get('name','')
    userid=request.session.get('userid','')
    if(resname==''):
        return HttpResponse('ERROR')
    else:




        #申请开始
        with connection.cursor() as cursor:
            sql = 'select id from userModel_resource where name = "'+ resname +'"'
            cursor.execute(sql)
            try:
                id = cursor.fetchall()
                sql = 'insert into userModel_record(startdate,enddate,extras,state,resource_id,user_id)' \
                      ' values("'+str(dic['beginDate'])+'","'+str(dic['endDate'])+'","'+dic['extras']+'","处理中","'+str(id[0][0])+'","'+str(userid)+'")'
                print(sql)
                cursor.execute(sql)
                cursor.close()
                return redirect('/my_application/')
            except:
                return HttpResponse('没有这个资源')

def addresource(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')


def delresource(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')
    if (request.method == 'POST'):
        changeitems = request.POST.getlist('shift', [])
        print(changeitems)
        thispage = request.GET.get('page', '')
        sqlread = 'delete from userModel_resource'
        sql2 = 'delete from userModel_resourcebelonging'
        sql1 = 'delete from userModel_record'
        if (len(changeitems) != 0):
            sqlread += ' where id in ('
            sql2 +=' where resource_id in('
            sql1 += ' where resource_id in('
            group = '('
            for id in changeitems:
                sql2 += ' ' + id + ','
                sqlread += ' ' + id + ','
                sql1+= ' ' + id + ','
                group += ' ' + id + ','
            sqlread = sqlread[:-1] + ')'
            sql2 = sql2[:-1]+')'
            sql1 = sql1[:-1] + ')'
            group = group[:-1]+')'

            resnamesql = 'select id,name from userModel_resource where id in '+group
            with connection.cursor() as cursor:
                cursor.execute(resnamesql)
                rs=cursor.fetchall()

                if(len(rs)!=0):
                    for item in rs:
                        resname = item[1]
                        id = item[0]
                        text = resname + ':资源已被删除，您的申请记录已取消'
                        restxt = resname + ':资源已取消，您不再拥有这个资源'
                        sql = 'select user_id from userModel_record where resource_id = "' + str(id) + '"'
                        cursor.execute(sql)
                        res = cursor.fetchall()
                        sql = 'insert into userModel_othernotice(text,isread,user_id) values("{}","False","{}")'
                        if (len(res) != 0):
                            for item in res:
                                id = item[0]  # 获取影响的用户id
                                sqltemp = sql.format(text, str(id))
                                cursor.execute(sqltemp)
                        else:
                            print("没有人租用这个资源")

                        sql = 'select owner_id from userModel_resourcebelonging where resource_id = "{}"'
                        sql = sql.format(str(id))
                        cursor.execute(sql)
                        res = cursor.fetchall()
                        sql = 'insert into userModel_othernotice(text,isread,user_id) values("{}","False","{}")'
                        if (len(res) != 0):
                            for item in res:
                                id = item[0]
                                sqltemp = sql.format(restxt, id)
                                cursor.execute(sqltemp)
                        else:
                            print('error ! 没有人拥有这个资源')


            #执行删除
            with connection.cursor() as cursor:
                cursor.execute(sql1)
                cursor.execute(sql2)
                cursor.close()
            with connection.cursor() as cursor:
                cursor.execute(sqlread)
                return redirect('/myresource/?page=1')
            return HttpResponse(sqlread)
        else:
            return redirect('/myresource/?page='+thispage)


def addresource(request):
    username = checksession(request)
    if (username == False):
        return redirect('/login')
    if(request.method == 'POST'):
        name = request.POST.get('name','')
        accountname = request.POST.get('account','')
        type = request.POST.get('type','')
        address = request.POST.get('address','')
        sqlcheck = 'select id from userModel_user where username = "'+str(accountname)+'"'
        sql = 'select id from userModel_resource where name = "' + name + '"'
        userid=0
        #检查用户
        with connection.cursor() as cursor:
            cursor.execute(sqlcheck)
            result = cursor.fetchall()
            if(len(result)!=0):
                userid= result[0][0]
            else:
                return render(request,"./add_resource.html",{"usernamealarm":'没有这个用户',"resourcenamealarm":''})
        #检查同名资源
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            if(len(result)!=0):
                return render(request, "./add_resource.html", {"usernamealarm": '', "resourcenamealarm": '已经有同名的资源了'})
        if(userid!= 0):
            with connection.cursor() as cursor:
                sql = 'insert into userModel_resource(name,type,isavailable,isborrowed,location) values("'+ str(name) +'","'+ str(type) +'","False","false","'+ str(address) +'")'
                print(sql)
                cursor.execute(sql)
                sql = 'select id from userModel_resource where name = "'+ str(name) +'"'
                cursor.execute(sql)
                result=cursor.fetchall()
                if(len(result)!=0):
                    id = result[0][0]
                    sql = 'insert into userModel_resourcebelonging(owner_id,resource_id) values("'+str(userid)+'","'+str(id)+'")'
                    print(sql)
                    cursor.execute(sql)
                return redirect('/myresource/?page=1')

def resadd(request):
    return render(request,"./add_resource.html",{"usernamealarm":'',"resourcenamealarm":''})


def cleanuser():
    sql = 'select id from userModel_user where enddate< date("now")'
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        if(len(result)!=0):
            for item in result:
                sqldelrecord='delete from userModel_record where user_id = {}'
                sqldelrecord.format(item[0])
                cursor.execute(sqldelrecord)

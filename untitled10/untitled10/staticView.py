from django.shortcuts import render,HttpResponse,redirect
from .dericLeung import checksession
def myResource(request):
    username=checksession(request)
    if(username==False):
        return redirect('/login')
    return render(request,"./resource_management.html",{'username':username},{'username':username})
def notice(request):
    username=checksession(request)
    if(username==False):
        return redirect('/login')
    return render(request,"./notice.html",{'username':username})
def myApplication(request):
    username=checksession(request)
    if(username==False):
        return redirect('/login')
    return render(request,"./my_application.html",{'username':username})
def roomclass(request):
    username=checksession(request)
    if(username==False):
        return redirect('/login')
    return render(request,"./roomclass_select.html",{'username':username})
def manage(request):
    username=checksession(request)
    if(username==False):
        return redirect('/login')
    return render(request,"./person_management.html",{'username':username})
def add(request):
    username=checksession(request)
    if(username==False):
        return redirect('/login')
    return render(request,"./person_add.html",{'username':username})
def dell(request):
    username=checksession(request)
    if(username==False):
        return redirect('/login')
    return render(request,"./person_del.html",{'username':username})
def adddel(request):
    username=checksession(request)
    if(username==False):
        return redirect('/login')
    return render(request,"./person_adddel.html",{'username':username})
def borrowableTable(request):
    username=checksession(request)
    if(username==False):
        return redirect('/login')
    return render(request,"./resource_borrowable.html",{'username':username})
def index(request):
    username=checksession(request)
    if(username==False):
        return redirect('/login')
    return render(request,"./index.html",{'username':username})
def fillTable(request):
    username=checksession(request)
    if(username==False):
        return redirect('/login')
    name = request.GET.get('name','')
    return render(request,"./booking_table.html",{'username':username,'name':name})
def login(request):
    return render(request,"./login.html")
def cancel_reserver(request):
    username=checksession(request)
    if(username==False):
        return redirect('/login')
    return render(request, "./cancel_reserve.html",{'username':username})
def detail(request):
    username=checksession(request)
    if(username==False):
        return redirect('/login')
    return render(request, "./detail.html",{'username':username})
def personal_information(request):
    username=checksession(request)
    if(username==False):
        return redirect('/login')
    return render(request, "./personal_information.html",{'username':username})
def my_resource(request):
    username=checksession(request)
    if(username==False):
        return redirect('/login')
    return render(request, "./my_resource.html",{'username':username})
def else_notice(request):
    username=checksession(request)
    if(username==False):
        return redirect('/login')
    return render(request, "./else_notice.html",{'username':username})
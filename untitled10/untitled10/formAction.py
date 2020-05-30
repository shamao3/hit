from django.http import HttpResponse
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
        usercode = request.POST.get("usercode")
        name = request.POST.get("name")
        password = request.POST.get("password")
        startDate = request.POST.get("startDate")
        endDate = request.POST.get("endDate")
        return HttpResponse("usercode:"+usercode+";name:"+name+";password:"+password+";startDate:"+startDate+";endDate:"+endDate)
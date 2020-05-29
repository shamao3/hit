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
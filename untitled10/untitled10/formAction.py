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
        return HttpResponse("usercode:" + usercode + ";name:" + name + ";password:" + password + ";startDate:"
                            + startDate + ";endDate:" + endDate)
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

def get_resManagement_Info(request):
    if(request.method == "POST");
        resName = request.POST.get("shift")

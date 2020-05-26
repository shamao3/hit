from django.shortcuts import render,HttpResponse

def myResource(request):
    return render(request,"./reserve_record.html");
def personal_center(request):
    return render(request,"./personal_center.html");
def notice(request):
    return render(request,"./notice.html");
def myApplication(request):
    return render(request,"./my_application.html");
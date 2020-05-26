from django.shortcuts import render,HttpResponse

def myResource(request):
    return render(request,"./reserve_record.html");
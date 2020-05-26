from django.shortcuts import render,HttpResponse

def myResource(request):
    return render(request,"./reserve_record.html");
def roomclass(request):
    return render(request,"./roomclass_select.html");
def manage(request):
    return render(request,"./person_management.html");
def adddel(request):
    return render(request,"./person_adddel.html");
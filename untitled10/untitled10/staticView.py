from django.shortcuts import render,HttpResponse

def myResource(request):
    return render(request,"./resource_management.html");
def personal_center(request):
    return render(request,"./personal_center.html");
def notice(request):
    return render(request,"./notice.html");
def myApplication(request):
    return render(request,"./my_application.html");
def roomclass(request):
    return render(request,"./roomclass_select.html");
def manage(request):
    return render(request,"./person_management.html");
def adddel(request):
    return render(request,"./person_adddel.html");
def borrowableTable(request):
    return render(request,"./resource_borrowable.html");
def index(request):
    return render(request,"./index.html");
def fillTable(request):
    return render(request,"./booking_table.html");


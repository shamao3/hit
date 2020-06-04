from django.db import connection,models
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils import timezone
import datetime
from datetime import date


def registered(request):
    request.session.clear_expired()
    if request.method == "POST":
        username = request.POST.get('userName')
        name = request.POST.get('name')
        password = request.POST.get('password')
        startdate = request.POST.get('startDate')
        enddate = request.POST.get('endDate')
        INSERT
        INTO
        userModel_user(name,userName,password,startdate,enddate)
        VALUES(username,name,password,startdate,enddate)


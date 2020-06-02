from django.db import models
from django.utils import timezone
# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20)
    userName = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    privilige = models.CharField(max_length=20)
    startdate = models.DateField()
    enddate = models.DateField()

class UserRelationship(models.Model):
    upperuser = models.ForeignKey('User',related_name="upperuser",on_delete=models.CASCADE)
    childuser = models.ForeignKey('User',related_name="childuser",on_delete=models.CASCADE)

class Resource(models.Model):
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    isavailable = models.BooleanField(default=False)
    isborrowed = models.BooleanField(default=False)
    location = models.CharField(max_length=20)

class ResourceBelonging(models.Model):
    owner = models.ForeignKey('User',on_delete=models.CASCADE)
    resource = models.ForeignKey('Resource',on_delete=models.CASCADE)

class OtherNotice(models.Model):
    text = models.CharField(max_length=200)
    isread = models.BooleanField(default=False)
    user = models.ForeignKey('User',on_delete=models.CASCADE)

class Record(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    resource = models.ForeignKey('Resource',on_delete=models.CASCADE)
    startdate = models.DateField()
    enddate = models.DateField()
    extras = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
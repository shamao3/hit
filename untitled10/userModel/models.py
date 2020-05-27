from django.db import models
from django.utils import timezone
# Create your models here.
class User(models.Model):
    userName = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    upperId = models.IntegerField(default=1)
from django.db import models
from django.db.models.fields import DateField, IntegerField
from django.contrib.auth.models import User
# Create your models here.



class Admin(models.Model):

    username=models.CharField(max_length=50,default='SOME STRING')
    password=models.CharField(max_length=25)

    '''
    OTHER IMPORTANT INFORMATION
    '''
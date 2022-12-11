from django.db import models
from django.db.models.fields import DateField, IntegerField
from django.contrib.auth.models import User
# Create your models here.






class strategy(models.Model):
    username=models.CharField(max_length=10,default="NONE")
    angel_api_keys=models.CharField(max_length=100,default='NONE')
    angel_client_id=models.CharField(max_length=10,default='NONE')
    angel_password=models.CharField(max_length=100,default='NONE')
    angel_token=models.CharField(max_length=100,default='NONE')

    lots=models.IntegerField(default=1)
    paper=models.CharField(default="off",max_length=4)
    bot=models.CharField(default="on",max_length=4)
    weekly_expiry=models.CharField(default="NONE",max_length=10)
    monthly_expiry=models.CharField(default="NONE",max_length=10)
    bots_started=models.IntegerField(default=0)
    shift_position=models.CharField(default="on",max_length=10)


class positions(models.Model):


    symbol=models.CharField(max_length=20,default='NA')
    time_in=models.DateTimeField(auto_now_add = True)
    price_in=models.FloatField(default=0)
    side = models.CharField(max_length=20,default='NA')
    current_price=models.FloatField(default=0)
    time_out=models.DateTimeField(default=0)
    price_out=models.FloatField(default=0)
    status=models.CharField(max_length=20,default='NA')
    token=models.CharField(max_length=20,default='NA')
    pnl=models.FloatField(default=0)
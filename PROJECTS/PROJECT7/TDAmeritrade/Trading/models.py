from django.db import models
import datetime

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    permission = models.CharField(max_length=20, default="admin")
    td_refresh_token = models.TextField(default='')
    td_consumer_key = models.TextField(default='')

    def __str__(self):
        return self.name

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50)
    sure_name = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    permission = models.IntegerField(default=2)
    td_refresh_token = models.TextField()
    td_consumer_key = models.TextField(default="")

class Bot(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="bot_owner", on_delete=models.PROTECT, blank=True, null=True)
    type = models.CharField(max_length=20, default="paper")
    side = models.CharField(max_length=20, default="Call")
    name = models.CharField(max_length=100)
    entry = models.TextField(default="")
    close = models.TextField(default="")
    symbol = models.CharField(max_length=10)
    amount = models.FloatField(default=0.0)
    status = models.BooleanField(default=False)

class Strategy(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name='strategy_user', on_delete=models.PROTECT, blank=True, null=True)
    part = models.CharField(max_length=10, default="1")
    position = models.CharField(max_length=20, default="")
    content = models.TextField(default="")

    def __str__(self):
        return self.name

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    bot_id = models.IntegerField(default=1)
    order_id = models.IntegerField(default=0)
    order_type = models.CharField(max_length=20)
    price = models.FloatField(default=0)
    duration = models.CharField(max_length=20)
    instruction = models.CharField(max_length=20)
    quantity = models.FloatField(default=1)
    symbol = models.CharField(max_length=20)
    asset_type = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    time = models.IntegerField(default=0)
    #datetime = models.DateTimeField(default=datetime.datetime.now())
    datetime = models.CharField(max_length=50)






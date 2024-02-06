
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,  login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse


from .helpful_scripts.strategy import *
from .helpful_scripts.background_functions import *
from .models import *

import threading
import random
import string
import json
import certifi
import ast

import logging
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger('dev_log')
error = logging.getLogger('error_log')

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
data={}
with open("background.json") as json_file:
    data=json.load(json_file)

client = MongoClient(data['mongo_uri'], server_api=ServerApi('1'),connect=False,tlsCAFile=certifi.where())
database=client[data['database']]
admin=database['admin']
position=database['position']
current_candles=database['candles']


def login_page(request):
    return render(request, "login.html")

def handleLogin(request):

    if request.user.is_authenticated:
        return redirect('/start_strategy')
    if request.method == "POST":

        loginusername = request.POST['username']
        loginpassword = request.POST['password']
        # user = authenticate(username=loginusername, password=loginpassword)
        if loginusername=="bybit_bot" and loginpassword=="bot_to_trade":
            user=User.objects.get(username=loginusername)
            login(request, user)
            return redirect("../start_strategy/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/")
    return redirect("/")

@login_required(login_url='')
def handleLogout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='')
def rest_update(request):
    data={}
    data['admin']=admin.find_one()
    positions=list(position.find())
    data['candles_data']=current_candles.find_one()['data']
    if data['admin']:
        data['admin']['_id'] = str(data['admin']['_id'])
    for pos in positions:
        pos['_id'] = str(pos['_id'])
    data['present_positions']=[]
    data['closed_positions']=[]

    for pos in positions:
        if(pos['status']=="OPEN"):
            data['present_positions'].append(pos)
        else:
            data['closed_positions'].append(pos)

    return JsonResponse(data)

@login_required(login_url='')
def start_strategy(request):
    data={}
    data['admin']=admin.find_one()
    positions=list(position.find())
    data['present_positions']=[]
    data['closed_positions']=[]

    for pos in positions:
        if(pos['status']=="OPEN"):
            data['present_positions'].append(pos)
        else:
            data['closed_positions'].append(pos)

    if request.method == "POST":
        recieved_data=request.POST
        recieved_data=recieved_data.copy()

        if('status' not in recieved_data):
            recieved_data['status']='off'
        if('live' not in recieved_data):
            recieved_data['live']='off'

        params={
            "api_key":recieved_data['api_key'],
            "secret_key":recieved_data['secret_key'],
            "investment":float(recieved_data['investment']),
            "symbols":ast.literal_eval(recieved_data['symbols']),
            "status":True if recieved_data['status']=='on' else False,
            "live":True if recieved_data['live']=='on' else False,
            "EMA_1_period":int(recieved_data['EMA_1_period']),
            "EMA_2_period":int(recieved_data['EMA_2_period']),
            "time_frame":recieved_data['time_frame'],
            "stoploss":float(recieved_data['stoploss']),
            "takeprofit":float(recieved_data['takeprofit'])
        }
        admin.update_one({},{"$set":params})
        print(params)
        data['admin']=admin.find_one()
        positions=list(position.find())

        return render(request, "index.html",data)
    return render(request, "index.html",data)


def do_something():
    logger.info("LOGGING STARTED")
    strat = run_strategy()
    value=strat.run()

def TESTING(request):
    return JsonResponse({"INSTANCE_COUNT":str(run_strategy.count)})

t=threading.Thread(target=do_something)
t.start()
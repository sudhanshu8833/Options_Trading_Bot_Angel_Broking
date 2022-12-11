import logging
from django.http import HttpResponse
import telepot
from datamanagement.helpful_scripts.background_functions import working_days
from django.shortcuts import render
from .helpful_scripts.strategy import *

# Create your views here.
from django.contrib import messages
import threading
from datamanagement.models import strategy
import random
import string
from .models import positions,  strategy
from datamanagement.helpful_scripts.background_functions import *
from smartapi import SmartConnect

from smartapi import SmartConnect
from smartapi import SmartWebSocket
logger = logging.getLogger('dev_log')


from .tasks import test_func

def test(request):
    test_func.delay()
    return HttpResponse("Done")

sleep_time=0

def data_calculation(request):
    global obj

    print("#############")

    logger.info("updated the system")
    t = threading.Thread(target=working_day_calculation, args=[0])
    t.setDaemon(True)
    t.start()

    print("#############")
    return render(request, "index.html")


def index(request):

    strategy1=strategy.objects.get(username="testing")
    return render(request, "index.html",{'list':strategy1})



def position(request):

    position = positions.objects.filter(status="OPEN")


    return render(request, "position.html",    {
        'list': position
    })


def closed_positions(request):

    position = positions.objects.filter(status="CLOSED")


    return render(request, "closed_position.html",    {
        'list': position
    })


def start_strategy(request):
    global sleep_time
    print(request)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    if request.method == "POST":

        lot = request.POST['lots']
        
        weeekly_expiry=request.POST['weekly_expiry']
        monthly_expiry=request.POST['monthly_expiry']


        strategy1=strategy.objects.get(username="testing")


        strategy1.angel_api_keys=request.POST['angel_api_keys']
        strategy1.angel_client_id=request.POST['angel_client_id']
        strategy1.angel_password=request.POST['angel_password']
        strategy1.angel_token=request.POST['angel_token']
        strategy1.lots=request.POST['lots']
        strategy1.weekly_expiry=request.POST['weekly_expiry']
        strategy1.monthly_expiry=request.POST['monthly_expiry']
        strategy1.bot=request.POST['bot']
        strategy1.paper=request.POST['paper']
        strategy1.shift_position=request.POST['shift_position']
        strategy1.save()



        # t = threading.Thread(target=do_something, args=[strategy1])
        # t.setDaemon(True)
        # t.start()
        # strategy1.bots_started=1
        strategy1.save()
        return render(request, "index.html",{'list':strategy1})



    strategy1=strategy.objects.get(username="testing")
    return render(request, "index.html",{'list':strategy1})

def do_something(strategy):



    strat = run_strategy(strategy)
    value=strat.run()
    if value!=None:
        return value



def random_string_generator(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))

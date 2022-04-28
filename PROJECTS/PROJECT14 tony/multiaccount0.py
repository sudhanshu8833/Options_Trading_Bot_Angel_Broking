# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
m=0


from finta import TA
import yfinance as yf
import requests
import time
import pandas as pd
import numpy as np
import datetime as dt
import json
import math
# from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from finta import TA
import yfinance as yf
import requests
import time
import pandas as pd
import numpy as np
import datetime as dt
import json
# from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

from datetime import date

import pandas as pd
import time
import sys

# local modules
from binance.client import Client
from binance.enums import *
# from indicator import indicators

# local file
import secrets

import yfinance as yf
import numpy as np
import datetime as dt
import requests 
import json 
import pandas as pd 
import numpy as np  
import requests
import time
import urllib
df3 = pd.read_csv("multiaccount.csv")

df1=df3.T
import threading


# %%
import telepot
bot = telepot.Bot('2064782147:AAER-p1y7290VzUYx_3swEvBFbtRUq39lBc')
bot.getMe()


# %%
def ltp_price(instrument,client):
    prices = client.get_all_tickers()
    for i in range(len(prices)):
        if prices[i]['symbol']==str(instrument):
            
            return float(prices[i]['price'])

def market_order(instrument,client,series):

    try:
        global df,dicts,quantity,df5

        ltp=ltp_price(instrument,client)

        data=client.futures_account_balance()
        for i in range(len(data)):
            if data[i]['asset']=='USDT':
                p_l=float(data[i]['withdrawAvailable'])   
        quantity=(((float(df5['stop_loss_percentage']['value0']))/100) * p_l)/ltp
        quantity=quantity*5
        quantity=quantity*1000


        quantity=math.floor(quantity)

        quantity=quantity/1000
        


        bot.sendMessage(1190128536,f"order quantity={quantity}, buy, {instrument} with p_l={p_l}")
        try:
            order = client.futures_create_order(
                symbol=str(instrument),
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
            
                
                quantity=quantity)
        except Exception as e:
            bot.sendMessage(1190128536,str(e))

        with open("signal.json") as json_data_file:
            data2 = json.load(json_data_file)
        data=data2['order_buy'][3]
        ltp=data2['order_buy'][3]['price']
        print(data)
        dict={}
        # dict[str(series['api key'])]=quantity
        dict['instrument']=instrument
        dict['quantity']=quantity
        dict['ltp']=ltp
        dicts.append(dict)
        bot.sendMessage(1190128536,str(dicts))
        l=1

    except Exception as e:
        print(str(e))
        bot.sendMessage(1190128536,str(e))


def market_order1(instrument,client,series):

    try:
        global df,quantity,dict,df5
        ltp=ltp_price(instrument,client)





        data=client.futures_account_balance()
        for i in range(len(data)):
            if data[i]['asset']=='USDT':
                p_l=float(data[i]['withdrawAvailable'])
        quantity=(((float(df5['stop_loss_percentage']['value0']))/100) * p_l)/ltp

        quantity=quantity*5
        quantity=quantity*1000


        quantity=math.floor(quantity)

        quantity=quantity/1000
        

        
        bot.sendMessage(1190128536,f'order quantity={quantity}, sold, {instrument} with p_l of {p_l}')
        try:
            order = client.futures_create_order(
                symbol=str(instrument),
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,

                
                quantity=quantity)
    
        except Exception as e:
            bot.sendMessage(1190128536,str(e))
        with open("signal.json") as json_data_file:
            data2 = json.load(json_data_file)
        data=data2['order_sell'][3]
        ltp=data2['order_sell'][3]['price']

        dict={}
        # dict[str(series['api key'])]=quantity
        dict['instrument']=instrument
        dict['quantity']=quantity
        dict['ltp']=ltp

        dicts.append(dict)
        bot.sendMessage(1190128536,str(dicts))
        l=1
    except Exception as e:
        print(str(e))
        bot.sendMessage(1190128536,str(e))
        


def close_position(instrument,order_type,client,series,data):
    global dicts
    try:

        value=data['order_close'][3]['price']

        for dict in dicts:
            if dict['ltp']==value:
                quantity1=dict['quantity']
                instrument1=dict['instrument']
                price=dict['ltp']
                dicts.remove(dict)
                break



        if order_type=='squareoffsell':
            bot.sendMessage(1190128536,f'order squareoff quantity={quantity1}, squareoffsell, {instrument1} with value of {value}')

            # pass
            order = client.futures_create_order(
            symbol=str(instrument1),
            side=Client.SIDE_SELL,
            type=Client.ORDER_TYPE_MARKET,


            quantity=round(float(quantity1),3))

        if order_type=='squareoffbuy':


            bot.sendMessage(1190128536,f'order squareoff quantity={quantity1}, squareoffbuy, {instrument1} with value of {value}')
            order = client.futures_create_order(
            symbol=str(instrument1),
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,

            
            quantity=round(float(quantity1),3))

    
        bot.sendMessage(1190128536,str(dicts))
    except Exception as e:

        bot.sendMessage(1190128536,str(e))


def market(client):
    global dicts,data3

    try:

        ltp=ltp_price(str(data3['symbol']),client)

        data=client.futures_account_balance()
        for i in range(len(data)):
            if data[i]['asset']=='USDT':
                p_l=float(data[i]['withdrawAvailable'])

        # p_l=float(client.futures_account_balance()[1]['withdrawAvailable'])
        # print(client.futures_account_balance())
        # print(p_l)
        quantity=(((float(data3['portfolio_percentage']))/100) * p_l)/ltp

        quantity=quantity*5
        quantity=quantity*1000


        quantity=math.floor(quantity)

        quantity=quantity/1000
        print(quantity)

        if data3['buy_sell']=='buy':

            # bot.sendMessage(1190128536,f'but buyed at {quantity}')
            # pass
            order = client.futures_create_order(
            symbol=str(data3['symbol']),
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,

            
            quantity=round(float(quantity),3))

        if data3['buy_sell']=='sell':
            # pass


            order = client.futures_create_order(
            symbol=str(data3['symbol']),
            side=Client.SIDE_SELL,
            type=Client.ORDER_TYPE_MARKET,

            quantity=round(float(quantity),3))



    except Exception as e:
        print(str(e))

        bot.sendMessage(1190128536,str(e))




# %%
def do_something(series):
    global df5,quantity,dict,data3
    client = Client(series['api key'],series['api secret key'])
    p_l=float(client.futures_account_balance()[1]['withdrawAvailable'])

    while True:
        try:

            with open("order.json") as json_data_file:
                data3 = json.load(json_data_file)  

            if data3['order']=='unfilled':
                market(client)    
                time.sleep(2)
                data3['order']='filled'
                json_object = json.dumps(data3, indent = 2)
                with open("order.json", "w") as outfile:
                    outfile.write(json_object)

            with open("signal.json") as json_data_file:
                data2 = json.load(json_data_file)

            if data2['order_buy'][2]=='unfilled':
                market_order(data2['order_buy'][1],client,series)
                time.sleep(2)
                data2['order_buy'][2]='filled'
                json_object = json.dumps(data2, indent = 2)
                with open("signal.json", "w") as outfile:
                    outfile.write(json_object)


            if data2['order_sell'][2]=='unfilled':
                market_order1(data2['order_sell'][1],client,series) 
                time.sleep(2)  
                data2['order_sell'][2]='filled'
                json_object = json.dumps(data2, indent = 2)
                with open("signal.json", "w") as outfile:
                    outfile.write(json_object)

            if data2['order_close'][2]=='unfilled':

                close_position(str(data2['order_close'][1]),str(data2['order_close'][0]),client,series,data2)
                time.sleep(2)
               
                data2['order_close'][2]='filled'
                json_object = json.dumps(data2, indent = 2)
                with open("signal.json", "w") as outfile:
                    outfile.write(json_object)


        except Exception as e:
            
            bot.sendMessage(1190128536,str(e))

# %%
dicts=[]

# try:

df4 = pd.read_csv("parameters.csv")
df4.set_index("parameters",inplace=True)
df5=df4.T

series=df1[:][m]
print(series)
do_something(series)


# except Exception as e:
#     print(e)


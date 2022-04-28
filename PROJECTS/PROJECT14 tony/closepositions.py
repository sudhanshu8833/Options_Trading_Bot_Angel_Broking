# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%

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
# def cancel_order():
#     global df1,df3
#     for i in range(len(df3)):

#         client = Client(df1[i]['api key'],df1[i]['api secret key'])
#         orders=client.futures_get_all_orders()
#         order=orders[-1]
#         print(order)
#         if order['side']=='SELL':
#             order = client.futures_create_order(
#                 symbol=str(order['symbol']),
#                 side=Client.SIDE_BUY,
#                 type=Client.ORDER_TYPE_MARKET,

                
#                 quantity=order['origQty'])


#         elif order['side']=='BUY':
#             order = client.futures_create_order(
#                 symbol=str(order['symbol']),
#                 side=Client.SIDE_SELL,
#                 type=Client.ORDER_TYPE_MARKET,

                
#                 quantity=order['origQty'])


# %%
def close_positions():

    global df1,df3
    for i in range(len(df3)):

        client = Client(df1[i]['api key'],df1[i]['api secret key'])
        orders=client.futures_position_information()
        for i in range(len(orders)):
            if round((float(orders[i]['positionAmt']))*1000,0)!=0:
                print(orders[i])
                order=orders[i]
                if (float(orders[i]['positionAmt']))*1000<0:
                    order1 = client.futures_create_order(
                        symbol=str(order['symbol']),
                        side=Client.SIDE_BUY,
                        type=Client.ORDER_TYPE_MARKET,

                        
                        # quantity=round(float(order['positionAmt']),3)
                        quantity=abs(float(order['positionAmt'])))

                if (float(orders[i]['positionAmt']))*1000>0:
                    order1 = client.futures_create_order(
                        symbol=str(order['symbol']),
                        side=Client.SIDE_SELL,
                        type=Client.ORDER_TYPE_MARKET,

                        
                        # quantity=round(float(order['positionAmt']),3)
                        quantity=abs(float(order['positionAmt'])))


# %%
close_positions()


# %%
# def open_positions():
#     global client
#     # log("Open positions:", color="blue")
#     client = Client(df1[0]['api key'],df1[0]['api secret key'])
#     open_position_count = 0
#     futures = client.futures_position_information()
#     for future in futures:
#         amount = future["positionAmt"]
#         if amount != "0" and float(future['unRealizedProfit']) != 0.00000000:  # if there is position
#             if future["entryPrice"] > future["liquidationPrice"]:
#                 open_position_count += 1
#                 print(future)



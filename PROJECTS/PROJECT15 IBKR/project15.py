# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import time
import numpy as np
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import pandas as pd
import yfinance as yf

client1 = oandapyV20.API(access_token="5feaa802c52be3e714d4bd74bc1a9169-8cbadb5f1a922e05aad7d56841b3f44a",environment="practice")
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
account_id = "101-002-19512089-001"
from ib_insync import *
util.startLoop()  # uncomment this line when in a notebook

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=56)

# %%

from finta import TA
import yfinance as yf
import requests
import time
import pandas as pd
import numpy as np
import datetime as dt
import json
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


client = Client("TRcoE5UH7baXbchQOoELzM7ck5t0deky7trYRZgNG3mM3N0KjNa06e1bX1GydT4u","WF4Ejhe0F3sldviu4HInSeZxD1jYBKVonfOALqKv3RnJmw1vjrXv5LcyYKLOvAS7")


# %%


def IBKR1():
    contracts = [Forex(pair) for pair in ('EURUSD', 'USDJPY', 'GBPUSD', 'USDCHF', 'USDCAD', 'AUDUSD')]
    ib.qualifyContracts(*contracts)

    eurusd = contracts[0]

    for contract in contracts:
        ib.reqMktData(contract, '', False, False)

    ticker = ib.ticker(eurusd)
    ib.sleep(.5)
    value=ticker.bid
    return float(value)

# %%
df=pd.DataFrame()

def bid_price():
    msft = yf.Ticker("EURUSD=X")

    # get stock info
    data=msft.info
    price=float(data['bid'])
    return price
# %%

params = {"instruments": "EUR_USD"}
account_id = "101-002-19512089-001"
r = pricing.PricingInfo(accountID=account_id, params=params)
i=0
# while True:
#     rv = client1.request(r)
#     # print("Time=",rv["time"])
#     print(rv["prices"][0]["closeoutBid"])
#     print(rv["prices"][0]["closeoutAsk"])
#     print("*******************")



# %%
binance=[]
IBKR=[]
btcusdt=[]
btceur=[]
times=[]
# %%
def main():
    global account_id,binance,IBKR,btcusdt,btceur,times
    params = {"instruments": "EUR_USD"}
    
    r = pricing.PricingInfo(accountID=account_id, params=params)
    rv = client1.request(r)
    # print(time.time())
    try:
        EUR_USD=IBKR1()
        # print(EUR_USD)
    except Exception as e:
        print(str(e))
        EUR_USD='N'

    try:
        BTC_USD=float(client.get_ticker(symbol='BTCUSDT')['bidPrice'])
        BTC_EUR=float(client.get_ticker(symbol='BTCEUR')['askPrice'])

    except:
        BTC_USD='N'
        BTC_EUR='N'

    # print(time.time())
    # binance.append(BTC_USD/BTC_EUR)
    btcusdt.append(BTC_USD)
    btceur.append(BTC_EUR)
    times.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    IBKR.append(EUR_USD)



times1=time.time()
while time.time()<60*60*3+times1:
    # times1=time.time()
    try:
    
        main()

    except Exception as e:
        print(str(e))
        # bot.sendMessage(1039725953,str(e))


# %%
df['time']=np.array(times)
df['BTC/USDT']=np.array(btcusdt)
df['BTC/EUR']=np.array(btceur)
# df['binance']=np.array(binance) #A/B
df['IBKR']=np.array(IBKR) #C


# profit=[]
# for i in range(len(df)):
#     profit.append(((df['IBKR'][i]-df['binance'][i])/df['IBKR'][i])*100)
    
# df['profit']=np.array(profit)
df.to_csv('testing2.csv')



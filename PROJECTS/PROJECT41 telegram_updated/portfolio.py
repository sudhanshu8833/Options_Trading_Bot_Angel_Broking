# %%
# importing the threading module


from datetime import date
import pandas as pd
import time
import sys
# local modules

from binance.client import Client
from binance.enums import *
from indicator import indicators
# local file
import traceback
import secrets
import json
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
from finta import TA
from multiprocessing import Process
from binance.client import BaseClient
import threading
import telepot
import pandas as pd

BaseClient.FUTURES_TESTNET_URL = 'https://fapi.binance.{}/fapi'
BaseClient.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'

client = Client("cc9feab03d1264ed67c07738cdd42502dd80a8b67fedaf2e5f9b6e9c55a2faad",
                "e30d3db72358639f29b6280bf1c54fd564e7b1eb5cb13f020739fd197f396e1b")


import datetime
# import pandas as pd
# bot = telepot.Bot('1715056219:AAGxytb3U1gIt1vlVn8Jf5b4za3E1HPuOd4')
# bot.getMe()



def ltp_price(instrument):
    prices = client.get_all_tickers()
    for i in range(len(prices)):
        if prices[i]['symbol'] == str(instrument):

            return float(prices[i]['price'])


# %%
df3 = pd.read_csv("account1.csv")
# df3.set_index("parameters",inplace=True)
# df2=df3.T

account1 = []
for i in range(len(df3)):
    api_key = df3['api key'][i]
    api_secret_key = df3['api secret key'][i]
    client = Client(str(api_key), str(api_secret_key))
    account1.append(client)

df3 = pd.read_csv("account2.csv")

account2 = []
for i in range(len(df3)):
    api_key = df3['api key'][i]
    api_secret_key = df3['api secret key'][i]
    client = Client(str(api_key), str(api_secret_key))
    account2.append(client)

df3 = pd.read_csv("account3.csv")

account3 = []
for i in range(len(df3)):
    api_key = df3['api key'][i]
    api_secret_key = df3['api secret key'][i]
    client = Client(str(api_key), str(api_secret_key))
    account3.append(client)

df3 = pd.read_csv("account4.csv")

account4 = []
for i in range(len(df3)):
    api_key = df3['api key'][i]
    api_secret_key = df3['api secret key'][i]
    client = Client(str(api_key), str(api_secret_key))
    account4.append(client)


def get_precision(symbol):
    global info
    for x in info['symbols']:
        if x['symbol'] == symbol:
            return x['quantityPrecision']


j = 0


def main(name, values, orders, value):

    df = pd.read_csv('portfolio_'+str(value)+'.csv')

    address=[]
    money=[]


    for client in name:
        data = client.futures_account_balance()
        for i in range(len(data)):
            if data[i]['asset'] == 'USDT':
                p_l = float(data[i]['withdrawAvailable'])
                address.append(client)
                money.append(p_l)

    x = datetime.datetime.now()
    column=str(x.date())
    df[column]=money

    df.to_csv('portfolio_'+str(value)+'.csv')








# %%

def f(name, value, orders):

    df3 = pd.read_csv("parameters.csv")
    values = df3[str(value)]
    print(values)
    if value == 'account1':
        time.sleep(1)

    if value == 'account2':
        time.sleep(2)

    if value == 'account3':
        time.sleep(3)

    main(name, values, orders, value)
    print(name)
# %%


info = client.futures_exchange_info()
orders = []
Processes = []
if __name__ == '__main__':

    Processes.append(Process(target=f, args=(account1, 'account1', orders)))
    Processes.append(Process(target=f, args=(account2, 'account2', orders)))
    Processes.append(Process(target=f, args=(account3, 'account3', orders)))
    Processes.append(Process(target=f, args=(account4, 'account4', orders)))


for process in Processes:
    process.start()


for process in Processes:
    process.join()

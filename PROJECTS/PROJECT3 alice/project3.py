# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from finta import TA
import yfinance as yf
import numpy as np
import pandas as pd
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import datetime as dt
import copy
import matplotlib.pyplot as plt
import time
import json
from csv import writer
from alice_blue import *
from configparser import ConfigParser
config=ConfigParser()
config.read('keys.conf')


from py5paisa import FivePaisaClient

client = FivePaisaClient(email="kkishor_powale@rediffmail.com", passwd="Hariom@1", dob="19860829")
client.login()
import telepot
bot = telepot.Bot('1930810344:AAGWYF0wwrPdj-KYwrUC7K01Zz0rwahKo18')
bot.getMe()


# %%
access_token = AliceBlue.login_and_get_access_token(username='AB063654', password='Omsairam@777', twoFA='a',  api_secret=config['ALICEBLUE']['App_secret'],app_id=config['ALICEBLUE']['App_ID'])


# %%
alice = AliceBlue(username='AB063654', password='Omsairam@777', access_token=access_token)


# %%
def candles(instrument):
    df=yf.download(instrument+'.NS',period='3mo',interval='1h')
    return df


# %%
investment=int(config['INPUTS']['investment'])
tickers=config['INPUTS']['tickers']
profit=float(config['INPUTS']['profit'])
falling=(float(config['INPUTS']['falling']))/100
High={}
price={}
position={}
stocks=[]
for ticker in tickers:
    High[ticker]=10000000
    position[ticker]=""
    price[ticker]=0


# %%
def Convert(string):
    li = list(string.split(","))
    return li
  
# Driver code    

tickers=Convert(tickers)


# %%
def selection1():
    global tickers,High,stocks,falling
    for ticker in tickers:
        print('analyzing for:', ticker)
    
        df=candles(ticker)
        high=df['High'][-7*42:-1].max()
        j=2
        if len(df)>=7*42:
            if df['Close'][-42*7]<df['Close'][-32*7]<df['Close'][-22*7]:
                for i in range(7*15):
                    if high-high*float(falling)<df['Low'][-7*15+i]<high:
                        j=1
                    
                    else:
                        j=2
                        break

        if j==2:
            continue
        
        stocks.append(ticker)
        High[ticker]=df['High'][-7*42:-1].max()



selection1()
bot.sendMessage(1039725953,"selected stocks for today")
bot.sendMessage(1039725953,stocks)


# %%
stocks


# %%
def market_order(instrument,investment):
    global price,order,order1,start_time,stock,order1,ltp,kickers


    price[instrument]=float(ltp)
    units=int(int(config['INPUTS']['investment'])/price[instrument])
    
    bot.sendMessage(1039725953,f"long position generated for {instrument} at {ltp}")
    # try:
    #     alice.place_order(transaction_type = TransactionType.Buy,
    #                 instrument = alice.get_instrument_by_symbol('NSE', str(instrument)),
    #                 quantity = units,
    #                 order_type = OrderType.StopLossMarket,
    #                 product_type = ProductType.Delivery,
    #                 price = None,
    #                 trigger_price = None,
    #                 stop_loss = float(ltp+ltp*profit),
    #                 square_off = None,
    #                 trailing_sl = None,
    #                 is_amo = False)
    # except Exception as e:
    #     print("Order placement failed: {}".format(e.message))


# %%
def position_now(instrument):
    data=alice.get_holding_positions()
    holdings=data['data']['holdings']
    signal=""
    for i in range(len(holdings)):
        if holdings[i]['trading_symbol']==instrument:
            signal="long"
                
    return signal

    
    


# %%
position_now("IOB")


# %%

def trade_signal(instrument,l_s):
    
    global High,ltp,falling,price1



    signal=""
    if l_s=="":
    
        if ltp<High[instrument]-falling*High[instrument]:
            signal="buy"
      
           
    return signal    


# %%

def main():
    global stocks,High,ltp,falling,price1
    

    for ticker in stocks:

        req_list_=[{"Exch":"N","ExchType":"C","Symbol":ticker}]
                    
        data=client.fetch_market_feed(req_list_)

        ltp=float(data['Data'][0]['LastRate'])

        print("\n \n analyzzing for ",ticker)
        print(ltp)

        l_s= position_now(ticker)
        
        print(l_s)
        if ltp==0:
            continue
        signal=trade_signal(ticker,l_s)


        if signal=='buy':
            
            

            market_order(ticker,investment)
            print("New long position initiated for ",ticker)


# %%
start_time=time.time()

timeout=start_time+60*60*5+45*60
times=time.time()

while time.time()<=timeout:

  
    main()
    print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

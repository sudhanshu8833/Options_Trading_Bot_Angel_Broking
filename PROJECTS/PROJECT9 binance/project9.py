# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from datetime import date

import pandas as pd
import time
import sys

# local modules
from binance.client import Client
from binance.enums import *
from indicator import indicators

# local file
import secrets
from configparser import ConfigParser
import yfinance as yf
import numpy as np
import datetime as dt
import requests 
import json 
import pandas as pd 
import numpy as np  
from finta import TA


# %%

#telegram authentification
import telepot
bot = telepot.Bot('1913570782:AAHIrTJDK7-toxsxqOv27Dh9wYU2d5HYfgk')
bot.getMe()


# %%
#reading 'parameters.csv'
df3 = pd.read_csv("parameters.csv")
df3.set_index("parameters",inplace=True)
df1=df3.T


# %%
bot.sendMessage(1039725953, 'BOT STARTED ....!!! HURRAY')
bot.sendMessage(665596324, 'BOT STARTED ....!!! HURRAY')



# %%

#logging in binance
client = Client((df1['binance_api_key'][0]), str(df1['binance_api_secret_key'][0]))


# %%

#historical data
def candle(symbol, interval):


    root_url = 'https://api.binance.com/api/v1/klines'
    url = root_url + '?symbol=' + symbol + '&interval=' + interval
    data = json.loads(requests.get(url).text)
    df = pd.DataFrame(data)
    df.columns = ['Datetime',
                'Open', 'High', 'Low', 'Close', 'volume',
                'close_time', 'qav', 'num_trades',
                'taker_base_vol', 'taker_quote_vol', 'ignore']
    df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.close_time]
    
    df.drop(['close_time','qav','num_trades','taker_base_vol', 'taker_quote_vol', 'ignore'],axis=1,inplace=True)
           
    
    df['Open']=pd.to_numeric(df["Open"], downcast="float")
    df["High"]=pd.to_numeric(df["High"], downcast="float")
    df["Low"]=pd.to_numeric(df["Low"], downcast="float")
    df["Close"]=pd.to_numeric(df["Close"], downcast="float")
    df["volume"]=pd.to_numeric(df["volume"], downcast="float")

    atr1='FIXED_ATR'
    df[atr1]=TA.ATR(df,int(df1['atr_fixed'][0]))
    df['X_BARS_HIGH']=df['High'][-int(df1['X_bars_high'][0]):-1].max()
    df['X_BARS_LOW']=df['Low'][-int(df1['X_bars_low'][0]):-1].min()

    atr=TA.ATR(df,int(df1['atr_trailing'][0]))
    

    df['TRAILING_ATR']=TA.ATR(df,int(df1['atr_trailing'][0]))
    

    return df


# %%

#getting latest price
def ltp_price(instrument):
    prices = client.get_all_tickers()
    for i in range(len(prices)):
        if prices[i]['symbol']==str(instrument):
            
            return float(prices[i]['price'])

    


# %%
#order function for buy
def market_order():
    global df,df1,distance_long,distance_short,buy_price,sell_price,quantity_buy,quantity_sell,fixed_buy_atr,fixed_sell_atr
    fixed_buy_atr=float(df['FIXED_ATR'][-1])

    p_l=float(client.futures_account_balance()[0]['balance'])
    stoploss=float(df1['stop_loss_precentage'][0])/100 * p_l
    quantity_buy=int(stoploss/fixed_buy_atr)
    # order = client.futures_create_order(
    #     symbol=str(df2['symbol_binance'][0]),
    #     side=Client.SIDE_BUY,
    #     type=Client.ORDER_TYPE_MARKET,
       
        
    #     quantity=float(df1['quantity'][0]))

    buy_price=ltp_price(df1['symbol_binance'][0])

    l=1
    


#order function for sell
def market_order1():
    global df,df1,distance_long,distance_short,buy_price,sell_price,quantity_buy,quantity_sell,fixed_buy_atr,fixed_sell_atr
    
    fixed_sell_atr=float(df['FIXED_ATR'][-1])


    p_l=float(client.futures_account_balance()[0]['balance'])
    stoploss=float(df1['stop_loss_precentage'][0])/100 * p_l
    quantity_sell=int(stoploss/fixed_sell_atr)


    

    # order = client.futures_create_order(
    #     symbol=str(df1['symbol_binance'][0]),
    #     side=Client.SIDE_SELL,
    #     type=Client.ORDER_TYPE_MARKET,


    #     quantity=float(df1['quantity'][0]))
    sell_price=ltp_price(df1['symbol_binance'][0])

    l=1





# %%
# klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")


# %%

#getting signal for buy/sell/squareoff's
def trade_signal(instrument,l_s):
    
    global df,df1,distance_long,distance_short,buy_price,sell_price,quantity_buy,quantity_sell,fixed_buy_atr,fixed_sell_atr,times1

    ltp=ltp_price(df1['symbol_binance'][0])

    

    signal=""
    if l_s=="":
        if time.time()>times1+300:

            times1=time.time()

        if ltp>float(df['X_BARS_HIGH'][-1]):
            signal="buy"
            



        if ltp<float(df['X_BARS_LOW'][-1]):
            signal="sell"



    elif l_s=="long":


        distance1_long=ltp-df['TRAILING_ATR'][-1]*float(df1['atr_trailing_multiplier'][0])
        if distance1_long>distance_long:
            distance_long=ltp-df['TRAILING_ATR'][-1]*float(df1['atr_trailing_multiplier'][0])

        if ltp<=buy_price-fixed_buy_atr*float(df1['atr_fixed_multiplier'][0]) or ltp<=distance_long:
            distance_long=0


            signal="squareoffsell"

        if time.time()>times1+300:



            times1=time.time()



    elif l_s=="short":
        distance1_short=ltp+df['TRAILING_ATR'][-1]*float(df1['atr_trailing_multiplier'][0])

        if distance1_short<distance_short:
            distance_short=ltp+df['TRAILING_ATR'][-1]*float(df1['atr_trailing_multiplier'][0])
        if ltp>=sell_price+fixed_sell_atr*float(df1['atr_fixed_multiplier'][0]) or ltp>=distance_short:
            distance_short=100000000000
            
            signal="squareoffbuy"


        if time.time()>times1+300:
            


            times1=time.time()


    return signal    


# %%


#main function
def main():
    global df,df1,distance_long,distance_short,buy_price,sell_price,quantity_buy,quantity_sell,fixed_buy_atr,fixed_sell_atr,position

 
    df3 = pd.read_csv("parameters.csv")
    df3.set_index("parameters",inplace=True)
    df1=df3.T
    ltp=ltp_price(df1['symbol_binance'][0])
    
    #for 'STOP BOT' and 'START BOT' command
    if df1['bot'].iloc[0]=='off':
        while True:
            position=''
            df3 = pd.read_csv("parameters.csv")
            df3.set_index("parameters",inplace=True)
            df1=df3.T
            if df1['bot'].iloc[-1]=='on':
                break

    #getting historical data
    df=candle(df1['symbol_binance'][0],str(df1['time_frame'][0]))
    print(df)






    
    
    # position=position_now(df1['symbol_binance'][0])
    signal=trade_signal(df1['symbol_binance'][0],position)

    
    
  

    #buying/selling/ squarring  off
    if signal=='buy':
        market_order()
        position='long'
        bot.sendMessage(1039725953,f"New long position initiated at {buy_price}")
        bot.sendMessage(665596324,f"New long position initiated at {buy_price}")
  
  

    if signal=='sell':
        market_order1()
        position='short'
        bot.sendMessage(1039725953,f"New short position initiated at {sell_price}")
        bot.sendMessage(665596324,f"New short position initiated at {sell_price}")
   
    
    if signal=="squareoffsell":
        market_order1()

        position=''
        bot.sendMessage(1039725953,f"long position squared of at {sell_price}")
        bot.sendMessage(665596324,f"long position squared of at {sell_price}")

        bot.sendMessage(1039725953,f" profit of {((sell_price-buy_price)/buy_price)*100*int(df1['binance_X'][0])}")
        bot.sendMessage(665596324,f" profit of {((sell_price-buy_price)/buy_price)*100*int(df1['binance_X'][0])}")
       
    if signal=="squareoffbuy":
        market_order()

        position=''
        bot.sendMessage(1039725953,f"short position squared of at {buy_price}")
        bot.sendMessage(665596324,f"short position squared of at {buy_price}")
     
        bot.sendMessage(1039725953,f" profit of {((sell_price-buy_price)/buy_price)*100*int(df1['binance_X'][0])}")
        bot.sendMessage(665596324,f" profit of {((sell_price-buy_price)/buy_price)*100*int(df1['binance_X'][0])}")
     





# %%


l=0
distance_short=100000000000
distance_long=0
times1=time.time()
position=''

#infinite loop
while True:
    try:

        main()
        print('hello')
    except Exception as e:
        botss=str(e)
        bot.sendMessage(1039725953,botss)





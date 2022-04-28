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
import math
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
df3 = pd.read_csv("parameters.csv")
df3.set_index("parameters",inplace=True)
df1=df3.T

client = Client("G5H5sixYr1dgeip4x43XMe02TIv6CKPluQNkSyTEZcelkfR6XowHXjdThDdP3Qkf","jPWgA6VPV0owVLleUQla2dKXmHpJ44gRf8yUK0Se707DpcqF5YeTDtZpmaDZzT8q")
with open("signal.json") as json_data_file:
    data2 = json.load(json_data_file)


# %%
# df=yf.download('MSFT',period='1mo',interval='5m')


# %%
import telepot
bot = telepot.Bot('2064782147:AAER-p1y7290VzUYx_3swEvBFbtRUq39lBc')
bot.getMe()


# %%
def candle_initial(symbol, interval,left,right):
    global j,Low_main,High_main,position

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
    l=0
    m=0

    High1_main=0
    for i in range(len(df)):
        if i<left:
            High1_main=0

        elif i>=left:
            if i==left:
                High1_main=df['High'].iloc[i]

            if i>left:
                # if (df['High'].iloc[i]>High1_main and m==0) or (m==0 and df['High'].iloc[i]>(df['High'][i-left:i]).max()):
                if (m==0 and df['High'].iloc[i]>(df['High'][i-left:i]).max()):
                    High1=df['High'].iloc[i]
                    
                    m=1

                if m==1:
                    if df['High'].iloc[i]<High1:
                        l+=1
                    else:
                        High1=df['High'].iloc[i]
                        l=0

        
                    if l>=right:
                        High1_main=High1
                        m=0
                        l=0 
    l=0
    m=0

    Low1_main=0
    for i in range(len(df)):
        if i<left:
            Low1_main=0

        elif i>=left:
            if i==left:
                Low1_main=df['Low'].iloc[i]

            if i>left:
                # if (df['Low'].iloc[i]<Low1_main and m==0) or (m==0 and df['Low'].iloc[i]<(df['Low'][i-left:i]).min()):
                if (m==0 and df['Low'].iloc[i]<(df['Low'][i-left:i]).min()):
                    Low1=df['Low'].iloc[i]
                    
                    m=1

                if m==1:
                    if df['Low'].iloc[i]>Low1:
                        l+=1
                    else:
                        Low1=df['Low'].iloc[i]
                        l=0


                    if l>=right:
                        Low1_main=Low1
                        m=0
                        l=0


    
    High_main[symbol]=High1_main
    Low_main[symbol]=Low1_main
    # bot.sendMessage(1190128536,f'High for {symbol} is {High_main[symbol]}')
    # # bot.sendMessage(621031629,f'High for {symbol} is {High_main[symbol]}')
    # bot.sendMessage(1190128536,f'Low for {symbol} is {Low_main[symbol]}')
    # # bot.sendMessage(621031629,f'Low for {symbol} is {Low_main[symbol]}')
    # bot.sendMessage(1190128536,f"{position[symbol]} for {symbol}")




    return df


# %%
# def candle(symbol, interval,left,right):
#     global j,k,High_main,Low_main,Low

#     root_url = 'https://api.binance.com/api/v1/klines'
#     url = root_url + '?symbol=' + symbol + '&interval=' + interval
#     data = json.loads(requests.get(url).text)
#     df = pd.DataFrame(data)
#     df.columns = ['Datetime',
#                 'Open', 'High', 'Low', 'Close', 'volume',
#                 'close_time', 'qav', 'num_trades',
#                 'taker_base_vol', 'taker_quote_vol', 'ignore']
#     df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.close_time]
    
#     df.drop(['close_time','qav','num_trades','taker_base_vol', 'taker_quote_vol', 'ignore'],axis=1,inplace=True)
    
    
#     df['Open']=pd.to_numeric(df["Open"], downcast="float")
#     df["High"]=pd.to_numeric(df["High"], downcast="float")
#     df["Low"]=pd.to_numeric(df["Low"], downcast="float")
#     df["Close"]=pd.to_numeric(df["Close"], downcast="float")
#     df["volume"]=pd.to_numeric(df["volume"], downcast="float")

    
    





#     if (df['High'].iloc[-1]>High_main[symbol] and k==0) or (k==0 and df['High'].iloc[-1]>(df['High'][-1-left:-1]).max()):
#         High[symbol]=df['High'].iloc[-1]
#         k=1

#     if k==1:
#         if df['High'].iloc[-1]<High[symbol]:
            
#             j=j+1

#         else:
#             High[symbol]=df['High'].iloc[-1]
#             j=0

#     if j>=right:
#         High_main[symbol]=High[symbol]
#         j=0
#         k=0
#         High[symbol]=0

#     if (df['Low'].iloc[-1]<Low_main[symbol] and k==0) or (k==0 and df['Low'].iloc[-1]<(df['Low'][-1-left:-1]).min()):
#         Low[symbol]=df['Low'].iloc[-1]
#         k=1

#     if k==1:
#         if df['Low'].iloc[-1]>Low[symbol]:
            
#             j=j+1

#         else:
#             Low[symbol]=df['Low'].iloc[-1]
#             j=0

#     if j>=right:
#         Low_main[symbol]=Low[symbol]
#         j=0
#         k=0
#         Low=0


#     return df


# %%
def ltp_price(instrument):
    prices = client.get_all_tickers()
    for i in range(len(prices)):
        if prices[i]['symbol']==str(instrument):
            
            return float(prices[i]['price'])


# %%
def market_order(instrument):

    try:
        global df,series,quantity,ltp
        # fixed_buy_atr=float(df['FIXED_ATR'][-1])
        # ltp=ltp_price(instrument)
        # p_l=float(client.futures_account_balance()[1]['withdrawAvailable'])
        # # stoploss=float(df1['stop_loss_percentage'][0])/100 * p_l
        # print(series['stop_loss_percentage'])
        # quantity=(((float(series['stop_loss_percentage']))/100) * p_l)/ltp
        # quantity=quantity*5
        # quantity=quantity*1000


        # quantity=math.floor(quantity)

        # quantity=quantity/1000
        
        # print(quantity)
        # print(p_l)
        # print(instrument)
        # print(ltp)
        with open("signal.json") as json_data_file:
            data2 = json.load(json_data_file)

        data2['order_buy'][1]=str(instrument)
        data2['order_buy'][2]='unfilled'
        data2['order_buy'][3]=orders[-1]

        dictionary =data2
        
        # Serializing json 
        json_object = json.dumps(dictionary, indent = 2)
        with open("signal.json", "w") as outfile:
            outfile.write(json_object)

        # bot.sendMessage(1190128536,quantity)

        # order = client.futures_create_order(
        #     symbol=str(instrument),
        #     side=Client.SIDE_BUY,
        #     type=Client.ORDER_TYPE_MARKET,
        
            
        #     quantity=quantity)

        # buy_price[instrument]=ltp_price(df1['symbol_binance'][0])


        
        l=1
    
    except Exception as e:
        bot.sendMessage(1190128536,str(e))


def market_order1(instrument):

    try:
        global df,series,quantity
        # ltp=ltp_price(instrument)
    # fixed_sell_atr=float(df['FIXED_ATR'][-1])


        # p_l=float(client.futures_account_balance()[1]['withdrawAvailable'])
        # print(series['stop_loss_percentage'])
        # quantity=(((float(series['stop_loss_percentage']))/100) * p_l)/ltp
        # # stoploss=float(df1['stop_loss_percentage'][0])/100 * p_l

        # # quantity_sell=int(stoploss/fixed_buy_atr)
        # quantity=abs(round(quantity*5,3))
        

        with open("signal.json") as json_data_file:
            data2 = json.load(json_data_file)

        data2['order_sell'][1]=str(instrument)
        data2['order_sell'][2]='unfilled'
        data2['order_sell'][3]=orders[-1]


        dictionary =data2

        # Serializing json 
        json_object = json.dumps(dictionary, indent = 2)
        with open("signal.json", "w") as outfile:
            outfile.write(json_object)


        # bot.sendMessage(1190128536,quantity)


        # order = client.futures_create_order(
        #     symbol=str(instrument),
        #     side=Client.SIDE_SELL,
        #     type=Client.ORDER_TYPE_MARKET,

            
        #     quantity=quantity)
            # sell_price[instrument]=ltp_price(df1['symbol_binance'][0])

        l=1
    except Exception as e:
        bot.sendMessage(1190128536,str(e))



def close_position(instrument,quantity,order_type,order):

    try:

        if order_type=='squareoffsell':

            with open("signal.json") as json_data_file:
                data2 = json.load(json_data_file)

            data2['order_close'][1]=str(instrument)
            data2['order_close'][0]=str(order_type)
            data2['order_close'][2]='unfilled'
            data2['order_close'][3]=order

            dictionary =data2

            # Serializing json 
            json_object = json.dumps(dictionary, indent = 2)
            with open("signal.json", "w") as outfile:
                outfile.write(json_object)

        if order_type=='squareoffbuy':

            with open("signal.json") as json_data_file:
                data2 = json.load(json_data_file)
            data2['order_close'][1]=str(instrument)
            data2['order_close'][0]=str(order_type)
            data2['order_close'][2]='unfilled'
            data2['order_close'][3]=order

            dictionary =data2
            
            # Serializing json 
            json_object = json.dumps(dictionary, indent = 2)
            with open("signal.json", "w") as outfile:
                outfile.write(json_object)


    except Exception as e:
        bot.sendMessage(1190128536,str(e))

# %%
def trade_signal(instrument,l_s):
    
    global df,ltp,orders,quantity



    ltp=ltp_price(instrument)
    # ltp=10000
    # print(series)
    print(ltp)
  
    signal=""
    if 'long' in l_s:
        # print(f'problem with {Low_main[instrument]} and {ltp}')
        if ltp>=High_main[instrument]:
            signal="buy"


    if 'short' in l_s:
        if ltp<=Low_main[instrument]:
            signal="sell"


    if len(orders)>0:
        print('aa rha hai')
        for i in range(len(orders)):

            if orders[i]['symbol_binance']==str(instrument) and orders[i]['order']=='long':
                if ltp>=float(orders[i]['price'])+float(orders[i]['takeprofit']):
                    signal='squareoffsell'
                    # bot.sendMessage(1190128536,f'position closed for {instrument} by takeprofit')
                    # bot.sendMessage(621031629,f'position closed for {instrument} by takeprofit')
                    

                elif ltp<=float(orders[i]['price'])-float(orders[i]['stoploss']):
                    signal='squareoffsell'
                    # bot.sendMessage(1190128536,f'position closed for {instrument} by stoploss')
                    # bot.sendMessage(621031629,f'position closed for {instrument} by stoploss')
                    

                elif orders[i]['trailing']=='off':
                    if ltp>float(orders[i]['price'])+float(orders[i]['trailing_after']):
                        
                        orders[i]['trailing']='on'
                        # bot.sendMessage(1190128536,f'trailing is activated for {instrument}')
                        # bot.sendMessage(621031629,f'trailing is activated for {instrument}')
                        
                elif orders[i]['trailing']=='on':

                    distance1_long[instrument]=ltp-float(orders[i]['trailing_for'])
                    if distance1_long[instrument]>distance_long[instrument]:
                        distance_long[instrument]=ltp-float(orders[i]['trailing_for'])
                    if ltp<=distance_long[instrument]:
                        distance_long[instrument]=0
                        
                        # bot.sendMessage(1190128536,f'position closed for {instrument} by trailing')
                        # bot.sendMessage(621031629,f'position closed for {instrument} by trailing')
                        signal="squareoffsell"  

                                    



            elif orders[i]['symbol_binance']==str(instrument) and orders[i]['order']=='short':
                if ltp<=float(orders[i]['price'])-float(orders[i]['takeprofit']):
                    signal='squareoffbuy'
                    # bot.sendMessage(1190128536,f'position closed for {instrument} by takeprofit')
                    # bot.sendMessage(621031629,f'position closed for {instrument} by takeprofit')
                    

                elif ltp>=float(float(orders[i]['price']))+float(orders[i]['stoploss']):
                    signal='squareoffbuy'
                    # bot.sendMessage(1190128536,f'position closed for {instrument} by stoploss')
                    # bot.sendMessage(621031629,f'position closed for {instrument} by stoploss')
                    

                elif orders[i]['trailing']=='off':
                    if ltp<float(orders[i]['price'])-float(orders[i]['trailing_after']):
                        # bot.sendMessage(1190128536,f'trailing is activated for {instrument}')
                        # bot.sendMessage(621031629,f'trailing is activated for {instrument}')
                        orders[i]['trailing']='on'

                elif orders[i]['trailing']=='on':

                    distance1_short[instrument]=ltp+float(orders[i]['trailing_for'])
                    if distance1_short[instrument]<distance_short[instrument]:
                        distance_short[instrument]=ltp+float(orders[i]['trailing_for'])
                    if ltp>=distance_short[instrument]:
                        distance_short[instrument]=0
                        distance1_short[instrument]=100000000000

                        signal="squareoffbuy"   
                        # bot.sendMessage(1190128536,f'position closed for {instrument} by trailing')
                        # bot.sendMessage(621031629,f'position closed for {instrument} by trailing')

            if signal=='squareoffbuy' or signal=='squareoffsell':
                bot.sendMessage(621031629,f'{orders[i]}')
                close_position(orders[i]['symbol_binance'],orders[i]['quantity'],signal,orders[i])
                print('position closed')
                bot.sendMessage(1190128536,f'position closed for {instrument} for {orders[i]["price"]}')
                bot.sendMessage(621031629,f'position closed for {instrument}')
                
                orders.pop(i)
                return signal  


            


    # elif l_s=="short":
    #     distance1_short[instrument]=ltp+df['TRAILING_ATR'][-1]*float(df1['atr_trailing_multiplier'][0])

    #     if distance1_short[instrument]<distance_short[instrument]:
    #         distance_short[instrument]=ltp+df['TRAILING_ATR'][-1]*float(df1['atr_trailing_multiplier'][0])
    #     if ltp>=sell_price[instrument]+fixed_sell_atr*float(df1['atr_fixed_multiplier'][0]) or ltp>=distance_short[instrument]:
    #         distance_short[instrument]=100000000000
    
    #         signal="squareoffbuy"




    return signal    


# %%
# times1=time.time()
# df3 = pd.read_csv("parameters.csv")
# df3.set_index("parameters",inplace=True)
# # print(df3)
# # series=df3['value'+str(1)].iloc[:]
# df1=df3.T
# print(df1['symbol_binance'])
# # print(df1)


# %%
def main():
    global High_main,j,k,Low_main,High,Low,series,orders,distance_long,distance_short,orders,tester_long,quantity

    
    df3 = pd.read_csv("parameters.csv")
    df3.set_index("parameters",inplace=True)
    df1=df3.T
    # series=df3[:].iloc[1]

    for i in range(len(df1)):
        series=df3['value'+str(i)].iloc[:]
        ticker=series['symbol_binance']
        # ltp=ltp_price(series['symbol_binance'])
        df=candle_initial(series['symbol_binance'],str(series['time_frame']),int(series['left']),int(series['right']))



    # series=df3['value0'].iloc[:]
    # print(series)
    # tickers=list(df1['symbol_binance'])


    while time.time()<=times1+60*1:
        for i in range(len(df1)):




            series=df3['value'+str(i)].iloc[:]

            ticker=series['symbol_binance']
            # ltp=ltp_price(series['symbol_binance'])
            # df=candle(series['symbol_binance'],str(series['time_frame']),int(series['left']),int(series['right']))
            # print('####################################')
            # print(f'analyzzing for {ticker}')
            # print(High_main[ticker])
            # print(Low_main[ticker])

 





            if position[ticker]=='short' and High_main[ticker]!=tester_long[ticker]:
                position[ticker]="long_short"
                tester_long[ticker]=0

            if position[ticker]=='long' and Low_main[ticker]!=tester_short[ticker]:
                position[ticker]="long_short"
                tester_short[ticker]=0
            
            # position=position_now(df1['symbol_binance'][0])
            signal=trade_signal(ticker,position[ticker])

            

        


            if signal=='buy':
                


                tester_long[ticker]=High_main[ticker]
                order={}
                order['symbol_binance']=str(ticker)
                order['price']=ltp
                order['trailing_for']=series['trailing_for']
                order['trailing_after']=series['trailing_after']
                order['trailing']='off'
                order['order']='long'
                order['stoploss']=series['stoploss']
                order['takeprofit']=series['takeprofit']
                order['quantity']=quantity
                orders.append(order)
                market_order(ticker)
                position[ticker]='short'

                dictionary ={
                    "order1":order,
                    
                }

                # Serializing json 
                json_object = json.dumps(dictionary, indent = 1)

                print(f"New long position initiated at {ltp}")
                bot.sendMessage(1190128536,f"New long position initiated at {ltp}")
                bot.sendMessage(621031629,f"New long position initiated at {ltp}")
                bot.sendMessage(1190128536,str(orders))



            if signal=='sell':
                
                tester_short[ticker]=Low_main[ticker]
                order={}
                order['symbol_binance']=str(ticker)
                order['price']=ltp
                order['trailing_for']=series['trailing_for']
                order['trailing_after']=series['trailing_after']
                order['trailing']='off'
                order['order']='short'
                order['stoploss']=series['stoploss']
                order['takeprofit']=series['takeprofit']
                order['quantity']=quantity
                
                orders.append(order)
                market_order1(ticker)
                dictionary ={
                    "order2":order,
                    
                }
                
                # Serializing json 
                json_object = json.dumps(dictionary, indent = 1)

                position[ticker]='long'
                bot.sendMessage(1190128536,f"New short position initiated at {ltp}")
                bot.sendMessage(621031629,f"New short position initiated at {ltp}")
                bot.sendMessage(1190128536,str(orders))


            # if signal=="squareoffsell":
            #     market_order1(ticker)



            #     print(f"long position squared of at {ltp}")
            #     # position[ticker]=''
            #     # bot.sendMessage(1190128536,f"long position squared of at {ltp}")
            #     # bot.sendMessage(1190128536,f" profit of {((sell_price[ticker]-buy_price[ticker])/buy_price[ticker])*100*int(df1['binance_X'][0])}")
            # if signal=="squareoffbuy":
            #     market_order(ticker)
            #     print(f"short position squared of at {ltp}")
            #     # position[ticker]=''
            #     # bot.sendMessage(1190128536,f"short position squared of at {ltp}")
            #     # bot.sendMessage(1190128536,f" profit of {((sell_price[ticker]-buy_price[ticker])/buy_price[ticker])*100*int(df1['binance_X'][0])}")



# %%
position={}
df3 = pd.read_csv("parameters.csv")
df3.set_index("parameters",inplace=True)
df1=df3.T


# %%



# %%
position={}
df3 = pd.read_csv("parameters.csv")
df3.set_index("parameters",inplace=True)
df1=df3.T
orders=[]
tickers=list(df1['symbol_binance'])
j=0
k=0
Low_main={}
Low={}
High_main={}
High={}
distance_long={}
distance_short={}
distance1_long={}
distance1_short={}
tester_long={}
tester_short={}
quantity=0
for i in range(len(df1)):
    series=df3['value'+str(i)].iloc[:]
    ticker=series['symbol_binance']
    Low_main[ticker]=0
    High_main[ticker]=0
    Low[ticker]=0
    High[ticker]=0
    position[ticker]=''
    candle_initial(ticker,str(series['time_frame']),int(series['left']),int(series['right']))
    ltp=ltp_price(ticker)
    print(ltp)
    print(High_main[ticker])
    print(Low_main[ticker])
    tester_long[ticker]=High_main[ticker]
    tester_short[ticker]=Low_main[ticker]
    if ltp>High_main[ticker]:
        position[ticker]='short'

    elif ltp<Low_main[ticker]:
        position[ticker]='long'

    else:
        position[ticker]="long_short"

    distance_long[ticker]=0
    distance_short[ticker]=100000000000
    distance1_long[ticker]=0
    distance1_short[ticker]=0

    
    print(High_main[ticker])
    print(Low_main[ticker])

    print(position[ticker])

while True:
    times1=time.time()
    try:

        main()

    except Exception as e:
        print(str(e))
        bot.sendMessage(1190128536,str(e))


# df3 = pd.read_csv("parameters.csv")
# df3.set_index("parameters",inplace=True)
# df1=df3.T
# tickers=df1['symbol_binance']
# list(tickers)

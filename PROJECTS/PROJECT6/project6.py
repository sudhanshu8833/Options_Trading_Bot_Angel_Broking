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
from indicator import indicators
from csv import writer

from smartapi import SmartConnect 
obj=SmartConnect(api_key="xucd0zCg")
data = obj.generateSession("S776051","Madhya246###")
refreshToken= data['data']['refreshToken']
feedToken=obj.getfeedToken()
userProfile= obj.getProfile(refreshToken)
import telepot
bot = telepot.Bot('1925707580:AAEbnYX47d9lzpr6Tk8V-XAIjqnJtcZQiv0')
bot.getMe()


df1 = pd.read_csv("project6.csv")


m=0


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
from indicator import indicators
from csv import writer

from smartapi import SmartConnect 
obj=SmartConnect(api_key="xucd0zCg")
data = obj.generateSession("S776051","Madhya246###")
refreshToken= data['data']['refreshToken']
feedToken=obj.getfeedToken()
userProfile= obj.getProfile(refreshToken)


def candles(instrument):
        
    ohlc_intraday=pd.DataFrame()

    historicParam={
    "exchange": "NSE",
    "symboltoken": str(instrument),
    "interval": "FIVE_MINUTE",
    "fromdate": "2021-07-05 09:15", 
    "todate": "2021-12-14 15:25"
    }

    data=obj.getCandleData(historicParam)

    data=pd.DataFrame(data)["data"]
    open=[]
    close=[]
    high=[]
    low=[]
    volume=[]
    index=[]
    for i in range(len(data)):
        open.append(data[i][1])

    for i in range(len(data)):
        close.append(data[i][4])

    for i in range(len(data)):
        high.append(data[i][2])

    for i in range(len(data)):
        low.append(data[i][3])

    for i in range(len(data)):
        index.append(data[i][0])

    for i in range(len(data)):
        volume.append(data[i][5])


    ohlc_intraday["Datetime"]=np.array(index)
    ohlc_intraday["Open"]=np.array(open)
    ohlc_intraday["High"]=np.array(high)
    ohlc_intraday["Low"]=np.array(low)

    ohlc_intraday["Close"]=np.array(close)
    ohlc_intraday["volume"]=np.array(volume)
    ohlc_intraday.set_index("Datetime",inplace=True)
    new_df = indicators.SuperTrend(ohlc_intraday,df1['big supertrend atr'][m],df1['big supertrend factor'][m])
    new_df = indicators.SuperTrend(ohlc_intraday,df1['small supertrend atr'][m],df1['small supertrend factor'][m])
    new_df=indicators.EMA(new_df,"Close","EMA25",25)
    return ohlc_intraday


# %%
def market_order():
    global price_buy,df1


    price_buy=obj.ltpData("NSE",str(df1['instrument symbol'][m])+'-EQ',str(df1['scrip code'][m]))['data']['ltp']
    # units=int(investment/price_buy)


    # try:
    #     orderparams = {
    #         "variety": "NORMAL",
    #         "tradingsymbol": str(df1['instrument symbol'][m])+'-EQ',
    #         "symboltoken": str(df1['scrip code'][m]),
    #         "transactiontype": "BUY",
    #         "exchange": "NSE",
    #         "ordertype": "MARKET",
    #         "producttype": "INTRADAY",
    #         "duration": "DAY",
        
            

    #         "quantity": str(abs(units))
    #         }
    #     orderId=obj.placeOrder(orderparams)
    #     print("The order id is: {}".format(orderId))
    #     bot.sendMessage(1060689126, 'long position generatted')
    # except Exception as e:
    #     print("Order placement failed: {}".format(e.message))
    
    



    



def market_order1():
    global price_sell,df1

    price_sell=obj.ltpData("NSE",str(df1['instrument symbol'][m])+'-EQ',str(df1['scrip code'][m]))['data']['ltp']
    # units=int(investment/price)




    # try:
    #     orderparams = {
    #         "variety": "NORMAL",
    #         "tradingsymbol": str(df1['instrument symbol'][m])+'-EQ',
    #         "symboltoken": str(df1['scrip code'][m]),
    #         "transactiontype": "SELL",
    #         "exchange": "NSE",
    #         "ordertype": "MARKET",
    #         "producttype": "INTRADAY",
    #         "duration": "DAY",


    #         "quantity": str(abs(units))
    #         }
    #     orderId=obj.placeOrder(orderparams)
    #     print("The order id is: {}".format(orderId))
    #     bot.sendMessage(1060689126, 'short position squared off')
    # except Exception as e:
    #     print("Order placement failed: {}".format(e.message))
    #     bot.sendMessage(1060689126, 'could not place the order ..... some error occurred')   


def trade_signal(l_s):
    
    global df,position,price_buy,price_sell,m,df1



    signal=""
    if l_s=="":
    
        if df.iloc[:,11][-1]!=df.iloc[:,11][-2] and position=="" and df.iloc[:,11][-1]=='up' and df.iloc[:,8][-1]=='up':
            signal="buy"
            position="long"
        
        elif df.iloc[:,11][-1]!=df.iloc[:,11][-2] and position=="" and df.iloc[:,11][-1]=='down' and df.iloc[:,8][-1]=='down':
            signal='sell'
            position='short'
            
      

    elif l_s=="long":
        if ltp>price_buy + price_buy*(float(df1['take profit'][m]))/100:
            
            signal="squareoffsell"
           
            position='None'

        elif ltp<price_buy - price_buy*(float(df1['stop loss'][m]))/100 and str(df1['stop loss recover'][m])=='yes':
            signal="squareoffsell"
            position="recovery_long"

        elif ltp<price_buy - price_buy*(float(df1['stop loss'][m]))/100 and str(df1['stop loss recover'][m])=='no':
            signal="squareoffsell"
            position='None'
                    
    elif l_s=="short":
        if ltp<price_sell - price_sell*(float(df1['take profit'][m]))/100:
            
            signal="squareoffbuy"
           
            position='None'

        elif ltp>price_sell + price_sell*(float(df1['stop loss'][m]))/100 and str(df1['stop loss recover'][m])=='yes':
            signal="squareoffbuy"
            position="recovery_short"

        elif ltp>price_sell + price_sell*(float(df1['stop loss'][m]))/100 and str(df1['stop loss recover'][m])=='no':
            signal="squareoffbuy"
            position='None'

    elif l_s=="recovery_long":
        if df.iloc[:,11][-1]!=df.iloc[:,11][-2] and df.iloc[:,11][-1]=='down' and df.iloc[:,8][-1]=='down' and df['Close'][-1]<df['EMA25'][-1]<df['Open'][-1]:
            signal="sell"
            position="recovery_long_short"
        


    elif l_s=="recovery_short":
        if df.iloc[:,11][-1]!=df.iloc[:,11][-2] and df.iloc[:,11][-1]=='up' and df.iloc[:,8][-1]=='up' and df['Open'][-1]<df['EMA25'][-1]<df['Close'][-1]:
            signal="buy"
            position="recovery_short_long"

    elif l_s=="recovery_long_short":
        if ltp<price_sell - price_sell*(float(df1['take profit'][m]))/100:
            
            signal="squareoffbuy"
    
            position=""

        elif ltp>price_sell + price_sell*(float(df1['stop loss'][m]))/100:
            signal="squareoffbuy"
            position="None"

    elif l_s=="recovery_short_long":
        if ltp>price_buy + price_buy*(float(df1['take profit'][m]))/100:
            
            signal="squareoffsell"
           
            position=""

        elif ltp<price_buy - price_buy*(float(df1['stop loss'][m]))/100:
            signal="squareoffsell"
            position="None"


    return signal    


# %%
position=""


def main():
    global ltp,position,price_buy,price_sell,df,df1
    
    try:
        df=candles(str(df1['scrip code'][m]))
        l_s=position
        signal=trade_signal(l_s)
        ltp=df['Close'][-1]

        if 'buy' in signal:
            if time.time()<=start_time+315*60:
                

                market_order()
                print("New long position initiated for ",df1['instrument symbol'][m])
                bot.sendMessage(1039725953,f"long position generated at {price_buy}")
                bot.sendMessage(1013979524,f"long position generated at {price_buy}")
        if 'sell' in signal:
            if time.time()<=start_time+315*60:
                market_order1()
                print("New short position initiated for ", df1['instrument symbol'][m])
                bot.sendMessage(1039725953,f"short position generated at {price_sell}")
                bot.sendMessage(1013979524,f"short position generated at {price_sell}")
        if 'squareoffbuy' in signal:
            market_order()
            print("short position squared off")
            bot.sendMessage(1039725953,f"short position squarred off at {price_buy}")
            bot.sendMessage(1013979524,f"short position squarred off at {price_buy}")
            time.sleep(300)
        if 'squareoffsell' in signal:
            market_order1()
            print("long position squared off")
            bot.sendMessage(1039725953,f"long position squarred off at {price_sell}")
            bot.sendMessage(1013979524,f"long position squarred off at {price_sell}")
            time.sleep(300)

    except Exception as e:

        print(e)



start_time=time.time()

timeout=start_time+60*60*5+45*60

while time.time()<=timeout:
    try:
        times1=time.time()
        main()
        
        print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        time.sleep(300-(time.time()-times1))

    except Exception as e:
        
        bot.sendMessage(1039725953, str(e))


if position=='long':
    bot.sendMessage(1039725953,f"long position squarred off at {price_sell}")
    bot.sendMessage(1013979524,f"long position squarred off at {price_sell}")

if position=="short":
    bot.sendMessage(1039725953,f"short position squarred off at {price_buy}")
    bot.sendMessage(1013979524,f"short position squarred off at {price_buy}")

if position=="recovery_long_short":
    bot.sendMessage(1039725953,f"short position squarred off at {price_buy}")
    bot.sendMessage(1013979524,f"short position squarred off at {price_buy}")

if position=="recovery_short_long":
    bot.sendMessage(1039725953,f"long position squarred off at {price_sell}")
    bot.sendMessage(1013979524,f"long position squarred off at {price_sell}")

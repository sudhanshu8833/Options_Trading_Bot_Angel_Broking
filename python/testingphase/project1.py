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
# time.sleep(56)
# we take the equity stocks which are also listed in F&O sction
# the code works on 5 minute candle stick 
# we start the code after 5 minutes of the start of the market
# conditions we want to be fulfilled are it should have a gap up opening + the first candle should be green 
# after 10 minutes of the start of the stock market we look for other condition that is, the close of the second candle should be higher then the high of second candle
# next condition we look for is the %range between todays open and close of second candle and we trade on one stock per day max, which is having this %range to be highest
# we buy trade when the high of the second candle gets hit, stoploss below .40% of the low of the same candle
# take profit at the end of the market time
# if it hits stoploss an another order of sell is generated
# stoploss for that order is atleast at .40% above the trade taken 
# for this short order as well we take profit at the end of todays market


# %%
import telepot
bot = telepot.Bot('1715056219:AAGxytb3U1gIt1vlVn8Jf5b4za3E1HPuOd4')
bot.getMe()


# %%
def candles(instrument):
        
    ohlc_intraday=pd.DataFrame()

    historicParam={
    "exchange": "NSE",
    "symboltoken": str(instrument),
    "interval": "FIVE_MINUTE",
    "fromdate": "2021-07-05 09:15", 
    "todate": "2021-08-14 15:25"
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


    ohlc_intraday["Index"]=np.array(index)
    ohlc_intraday["Open"]=np.array(open)
    ohlc_intraday["High"]=np.array(high)
    ohlc_intraday["Low"]=np.array(low)

    ohlc_intraday["Close"]=np.array(close)
    ohlc_intraday["Volume"]=np.array(volume)
    ohlc_intraday.set_index("Index",inplace=True)

    return ohlc_intraday


# %%
from smartapi import SmartConnect 
obj=SmartConnect(api_key="iJ3YYOXH")
data = obj.generateSession("S776051","Madhya246###")
refreshToken= data['data']['refreshToken']
feedToken=obj.getfeedToken()
userProfile= obj.getProfile(refreshToken)


# %%
from py5paisa import FivePaisaClient

client = FivePaisaClient(email="sudhanshu8833@gmail.com", passwd="Madhya246###", dob="20010626")
client.login()


# %%
bot.sendMessage(1039725953, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
tame=time.time()
# time.sleep(90)
kickers={'AARTIIND': 7, 'ABFRL': 30108, 'ACC': 22, 'ADANIENT': 25, 'ADANIPORTS': 15083, 'ALKEM': 11703, 'AMARAJABAT': 100, 'AMBUJACEM': 1270, 'APLLTD': 25328, 'APOLLOHOSP': 157, 'APOLLOTYRE': 163, 'ASHOKLEY': 212, 'ASIANPAINT': 236, 'AUBANK': 21238, 'AUROPHARMA': 275, 'AXISBANK': 5900, 'BAJAJ-AUTO': 16669, 'BAJAJFINSV': 16675, 'BAJFINANCE': 317, 'BALKRISIND': 335, 'BANDHANBNK': 2263, 'BANKBARODA': 4668, 'BATAINDIA': 371, 'BEL': 383, 'BERGEPAINT': 404, 'BHARATFORG': 422, 'BHARTIARTL': 10604, 'BHEL': 438, 'BIOCON': 11373, 'BOSCHLTD': 2181, 'BPCL': 526, 'BRITANNIA': 547, 'CADILAHC': 7929, 'CANBK': 10794, 'CHOLAFIN': 685, 'CIPLA': 694, 'COALINDIA': 20374, 'COFORGE': 11543, 'COLPAL': 15141, 'CONCOR': 4749, 'COROMANDEL': 739, 'CUB': 5701, 'CUMMINSIND': 1901, 'DABUR': 772, 'DEEPAKNTR': 19943, 'DIVISLAB': 10940, 'DLF': 14732, 'DRREDDY': 881, 'EICHERMOT': 910, 'ESCORTS': 958, 'EXIDEIND': 676, 'FEDERALBNK': 1023, 'GAIL': 4717, 'GLENMARK': 7406, 'GMRINFRA': 13528, 'GODREJCP': 10099, 'GODREJPROP': 17875, 'GRANULES': 11872, 'GRASIM': 1232, 'GUJGASLTD': 10599, 'HAVELLS': 9819, 'HCLTECH': 7229, 'HDFC': 1330, 'HDFCAMC': 4244, 'HDFCBANK': 1333, 'HDFCLIFE': 467, 'HEROMOTOCO': 1348, 'HINDALCO': 1363, 'HINDPETRO': 1406, 'HINDUNILVR': 1394, 'IBULHSGFIN': 30125, 'ICICIBANK': 4963, 'ICICIGI': 21770, 'ICICIPRULI': 18652, 'IDEA': 14366, 'IDFCFIRSTB': 11184, 'IGL': 11262, 'INDHOTEL': 1512, 'INDIGO': 11195, 'INDUSINDBK': 5258, 'INDUSTOWER': 29135, 'INFY': 1594, 'IOC': 1624, 'IRCTC': 13611, 'ITC': 1660, 'JINDALSTEL': 6733, 'JSWSTEEL': 11723, 'JUBLFOOD': 18096, 'KOTAKBANK': 1922, 'L&TFH': 11654, 'LALPATHLAB': 1997, 'LICHSGFIN': 19104, 'LT': 17395, 'LTI': 11483, 'LTTS': 17700, 'LUPIN': 17818, 'M&M': 18564, 'M&MFIN': 10440, 'MANAPPURAM': 19061, 'MARICO': 4067, 'MARUTI': 10999, 'MCDOWELL-N': 10447, 'METROPOLIS': 9581, 'MFSL': 2142, 'MGL': 17534, 'MINDTREE': 14356, 'MOTHERSUMI': 4204, 'MPHASIS': 4503, 'MRF': 2277, 'MUTHOOTFIN': 23650, 'NAM-INDIA': 357, 'NATIONALUM': 6364, 'NAUKRI': 13751, 'NAVINFLUOR': 14672, 'NESTLEIND': 17963, 'NMDC': 15332, 'NTPC': 11630, 'ONGC': 2475, 'PAGEIND': 14413, 'PEL': 2412, 'PETRONET': 11351, 'PFC': 14299, 'PFIZER': 2643, 'PIDILITIND': 2664, 'PIIND': 24184, 'PNB': 10666, 'POWERGRID': 14977, 'PVR': 13147, 'RAMCOCEM': 2043, 'RBLBANK': 18391, 'RECLTD': 15355, 'RELIANCE': 2885, 'SAIL': 2963, 'SBILIFE': 21808, 'SBIN': 3045, 'SHREECEM': 3103, 'SIEMENS': 3150, 'SRF': 3273, 'SRTRANSFIN': 4306, 'SUNPHARMA': 3351, 'SUNTV': 13404, 'TATACHEM': 3405, 'TATACONSUM': 3432, 'TATAMOTORS': 3456, 'TATAPOWER': 3426, 'TATASTEEL': 3499, 'TCS': 11536, 'TECHM': 13538, 'TITAN': 3506, 'TORNTPHARM': 3518, 'TORNTPOWER': 13786, 'TRENT': 1964, 'TVSMOTOR': 8479, 'UBL': 16713, 'ULTRACEMCO': 11532, 'UPL': 11287, 'VEDL': 3063, 'VOLTAS': 3718, 'WIPRO': 3787, 'ZEEL': 3812}

lickers=[]


# %%

investment=5000
risk=50   
portfolio=30000

prise=0
ltp=0

# selection()
# print(jikers)
# print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

ohlcv_database=pd.DataFrame()

order=[]
order1=[]
price=0

position=""




# %%
def selection1():
    global lickers,kickers
    for ticker in kickers:
        try:
            print('analyzing for:', ticker)
            print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            df=candles(kickers[ticker])

            req_list_=[{"Exch":"N","ExchType":"C","Symbol":ticker}]
                
            data=client.fetch_market_feed(req_list_)
            price=float(data['Data'][0]['PClose'])
                



            print("\n \n analyzzing for ",ticker)
            print(price)
            time.sleep(0.25)
            try:
                if df['Close'].iloc[-2]>df['Open'].iloc[-2] and ((price-df['Open'].iloc[-2])/price)*100>.5:
                    lickers.append(ticker)

            except Exception as e:
                print(e)
                bot.sendMessage(1039725953, e.message)
                bot.sendMessage(1039725953, e.args)

        except Exception as e:
            print(e)
            bot.sendMessage(1039725953, e.message)
            bot.sendMessage(1039725953, e.args)


# %%

selection1()
try:
    print(lickers)
    bot.sendMessage(1039725953, lickers)

except:
    print('couldn,t send message')
# print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


# %%
high={}
low=0
times=99999999999999999
high1=1000000000

for ticker in lickers:
    high[ticker]=1000000000


# %%



# %%
yickers=[]
value={}

for ticker in lickers:
    value[ticker]=0

def selection2():
    global lickers,yickers,high,kickers,value
    for ticker in lickers:
        print('analyzing for: ',ticker)
        df=candles(kickers[ticker])
        time.sleep(.25)
        try:
            if df['Close'].iloc[-1]>df['High'].iloc[-2]:
                yickers.append(ticker)
                value[ticker]=abs((df['Close'].iloc[-1]-df['Open'].iloc[-2])/df['Open'].iloc[-2])
                print(value[ticker])

                high[ticker]=df['High'].iloc[-1]

        except Exception as e:
            print(e)
            bot.sendMessage(1039725953, e)
  

        


# %%
# time.sleep(300-(time.time()-tame))
bot.sendMessage(1039725953, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
time.sleep(10)
selection2()


# %%
try:
    stock='hi'
    max=0
    for ticker in yickers:
        if value[ticker]>max:
            max=value[ticker]
            print(max)
            stock=ticker

except Exception as e:
    print(e)
    bot.sendMessage(1039725953, e)

stock='ADANIENT'
high=high[stock]
low=0


bot.sendMessage(1039725953, stock)


# %%
def market_order(instrument,investment,risk):
    global price,order,order1,start_time,stock,order1,ltp
    # if time.time()>=start_time+5700:

    #     continue

    price=float(ltp)    
    units=round(investment/price,0)
   
    if units>0:
        order=[]
        order.append(float(ltp))
        order.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        bot.sendMessage(1039725953, stock)
        bot.sendMessage(1039725953, "long position initiated for")
        bot.sendMessage(1039725953, price)

    

        order.append("long")



    elif units<0:

        order1=[]
        order1.append(float(ltp))
        order1.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        order1.append("short")
        price=float(ltp)
        bot.sendMessage(1039725953, stock)
        bot.sendMessage(1039725953, "short position and squaredoff")
        bot.sendMessage(1039725953, price)


    print("order filled for ",stock)



def market_order1(instrument,investment):
    global price,position,order,ltp,stock

    price=float(ltp)
    units=round(investment/price,0)



    if units>0:

        order1.append(float(ltp))
        order1.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        bot.sendMessage(1039725953, stock)
        bot.sendMessage(1039725953, 'shortposition squared off')
        bot.sendMessage(1039725953, price)
            




    if units<0:
        order.append(float(ltp))
 
        order.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        bot.sendMessage(1039725953, stock)
        bot.sendMessage(1039725953, 'squarred off at')
        bot.sendMessage(1039725953, price)



 
    print("order squared off for ",stock)


# %%
def trade_signal(instrument,l_s):
    
    global ltp,position,high,low,high1,stock,times,price



    signal=""
    if l_s=="":
    
        if ltp>high:
            signal="buy"
            times=time.time()
            position='long'

                        
      

    elif l_s=="long":
        if ltp<=low-low*.004:
            
            signal="sell and squareoffsell"
            times=time.time()
            position='short'
           
                    
    elif l_s=="short":
        if high1<price+price*.004:
            if ltp>=price+.004*price:
                signal="squareoffbuy"

        elif high1>price+price*.004:
            if ltp>=high1:
                signal='squareoffbuy'

            


    return signal    


# %%
def main():
    global investment,risk,ltp,position,prise,high,start_time,low,high1,kickers,stock,times
    
    try:

        df=candles(kickers[stock])
        timedate=time.localtime(time.time())
        t=timedate.tm_min%5
        tr=timedate.tm_min-t
        trr=timedate.tm_hour
        
        if position=='long' and str(trr)+':'+str(tr) in df.index[-2]:
            
                
                
            low=df['Low'].iloc[-2]

        if position=='short' and str(trr)+':'+str(tr) in df.index[-2]:

            
            high1=df['High'].iloc[-2]




        # req_list_=[{"Exch":"N","ExchType":"C","Symbol":stock}]
            
        # data=client.fetch_market_feed(req_list_)
        # ltp=float(data['Data'][0]['LastRate'])
            

        ltp+=1

        print("\n \n analyzzing for ",stock)
        print(ltp)


        l_s= position
        print(l_s)
        signal=trade_signal(stock,l_s)
        if 'buy' in signal:
            if time.time()<=start_time+5700:
        

                market_order(stock,investment,risk)
                print("New long position initiated for ",stock)

        if 'sell' in signal:
            market_order(stock,-1*investment,risk)
            print("New short position initiated for ", stock)

        if 'squareoffbuy' in signal:
            market_order1(stock,investment)

        if 'squareoffsell' in signal:
            market_order1(stock,-1*investment)
    
    except Exception as e:

        print(e)
        bot.sendMessage(1039725953, e)
        # bot.sendMessage(1039725953, e.args)


# %%

start_time=time.time()

timeout=start_time+60*10

while time.time()<=timeout:
    try:
  
        main()
        print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        bot.sendMessage(1039725953, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    except Exception as e:
        print(e)
        bot.sendMessage(1039725953, e.message)
        bot.sendMessage(1039725953, e.args)


# %%

# req_list_=[{"Exch":"N","ExchType":"C","Symbol":stock}]
    
# data=client.fetch_market_feed(req_list_)
# ltp=float(data['Data'][0]['LastRate'])        

print("\n \n analyzzing for ",stock)
print(ltp)
if position=="long":
    market_order1(stock,-1*investment)

if position=="short":
    market_order1(stock,investment)     


# %%
print(order)
print(order1)

bot.sendMessage(1039725953, order)
bot.sendMessage(1039725953, order1)


df=pd.DataFrame(order)
df=df.T
df.columns=["price_in","time_in","type","price_out","time_out"]
df["stocks"]=df.index



profit=[]
for i in range(len(df)):
    if df['type'][i]=='long':
        profit.append(((df['price_out'][i]-df['price_in'][i])/df['price_in'][i])*100)

    elif df['type'][i]=='short':
        profit.append(((df['price_in'][i]-df['price_out'][i])/df['price_out'][i])*100)

df["profit"]=np.array(profit)


df.to_csv("opg1111.csv")



df1=pd.DataFrame(order1)
df1=df.T
df1.columns=["price_in","time_in","type","price_out","time_out"]
df1["stocks"]=df1.index



profit=[]
for i in range(len(df1)):
    if df1['type'][i]=='long':
        profit.append(((df1['price_out'][i]-df1['price_in'][i])/df1['price_in'][i])*100)

    elif df1['type'][i]=='short':
        profit.append(((df1['price_in'][i]-df1['price_out'][i])/df1['price_out'][i])*100)

df1["profit"]=np.array(profit)


df1.to_csv("opg11112.csv")


# %%



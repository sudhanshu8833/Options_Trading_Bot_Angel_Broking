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




# %%
import telepot
bot = telepot.Bot('1909267145:AAFD0a_mHpsieVdSxgj_dej9LEFMYF7G_x8')
bot.getMe()


# %%
def candles(instrument):
    data=yf.download(instrument+'.NS',period='2d',interval='5min')




# %%
from py5paisa import FivePaisaClient

client = FivePaisaClient(email="jayeshpatel51999@gmail.com", passwd="jayesh@51999", dob="19791215")
client.login()


# %%
bot.sendMessage(1039725953, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


kickers={'AARTIIND': 7, 'ABFRL': 30108, 'ACC': 22, 'ADANIENT': 25, 'ADANIPORTS': 15083, 'ALKEM': 11703, 'AMARAJABAT': 100, 'AMBUJACEM': 1270, 'APLLTD': 25328, 'APOLLOHOSP': 157, 'APOLLOTYRE': 163, 'ASHOKLEY': 212, 'ASIANPAINT': 236, 'AUBANK': 21238, 'AUROPHARMA': 275, 'AXISBANK': 5900, 'BAJAJ-AUTO': 16669, 'BAJAJFINSV': 16675, 'BAJFINANCE': 317, 'BALKRISIND': 335, 'BANDHANBNK': 2263, 'BANKBARODA': 4668, 'BATAINDIA': 371, 'BEL': 383, 'BERGEPAINT': 404, 'BHARATFORG': 422, 'BHARTIARTL': 10604, 'BHEL': 438, 'BIOCON': 11373, 'BOSCHLTD': 2181, 'BPCL': 526, 'BRITANNIA': 547, 'CADILAHC': 7929, 'CANBK': 10794, 'CHOLAFIN': 685, 'CIPLA': 694, 'COALINDIA': 20374, 'COFORGE': 11543, 'COLPAL': 15141, 'CONCOR': 4749, 'COROMANDEL': 739, 'CUB': 5701, 'CUMMINSIND': 1901, 'DABUR': 772, 'DEEPAKNTR': 19943, 'DIVISLAB': 10940, 'DLF': 14732, 'DRREDDY': 881, 'EICHERMOT': 910, 'ESCORTS': 958, 'EXIDEIND': 676, 'FEDERALBNK': 1023, 'GAIL': 4717, 'GLENMARK': 7406, 'GMRINFRA': 13528, 'GODREJCP': 10099, 'GODREJPROP': 17875, 'GRANULES': 11872, 'GRASIM': 1232, 'GUJGASLTD': 10599, 'HAVELLS': 9819, 'HCLTECH': 7229, 'HDFC': 1330, 'HDFCAMC': 4244, 'HDFCBANK': 1333, 'HDFCLIFE': 467, 'HEROMOTOCO': 1348, 'HINDALCO': 1363, 'HINDPETRO': 1406, 'HINDUNILVR': 1394, 'IBULHSGFIN': 30125, 'ICICIBANK': 4963, 'ICICIGI': 21770, 'ICICIPRULI': 18652, 'IDEA': 14366, 'IDFCFIRSTB': 11184, 'IGL': 11262, 'INDHOTEL': 1512, 'INDIGO': 11195, 'INDUSINDBK': 5258, 'INDUSTOWER': 29135, 'INFY': 1594, 'IOC': 1624, 'IRCTC': 13611, 'ITC': 1660, 'JINDALSTEL': 6733, 'JSWSTEEL': 11723, 'JUBLFOOD': 18096, 'KOTAKBANK': 1922, 'L&TFH': 11654, 'LALPATHLAB': 1997, 'LICHSGFIN': 19104, 'LT': 17395, 'LTI': 11483, 'LTTS': 17700, 'LUPIN': 17818, 'M&M': 18564, 'M&MFIN': 10440, 'MANAPPURAM': 19061, 'MARICO': 4067, 'MARUTI': 10999, 'MCDOWELL-N': 10447, 'METROPOLIS': 9581, 'MFSL': 2142, 'MGL': 17534, 'MINDTREE': 14356, 'MOTHERSUMI': 4204, 'MPHASIS': 4503, 'MRF': 2277, 'MUTHOOTFIN': 23650, 'NAM-INDIA': 357, 'NATIONALUM': 6364, 'NAUKRI': 13751, 'NAVINFLUOR': 14672, 'NESTLEIND': 17963, 'NMDC': 15332, 'NTPC': 11630, 'ONGC': 2475, 'PAGEIND': 14413, 'PEL': 2412, 'PETRONET': 11351, 'PFC': 14299, 'PFIZER': 2643, 'PIDILITIND': 2664, 'PIIND': 24184, 'PNB': 10666, 'POWERGRID': 14977, 'PVR': 13147, 'RAMCOCEM': 2043, 'RBLBANK': 18391, 'RECLTD': 15355, 'RELIANCE': 2885, 'SAIL': 2963, 'SBILIFE': 21808, 'SBIN': 3045, 'SHREECEM': 3103, 'SIEMENS': 3150, 'SRF': 3273, 'SRTRANSFIN': 4306, 'SUNPHARMA': 3351, 'SUNTV': 13404, 'TATACHEM': 3405, 'TATACONSUM': 3432, 'TATAMOTORS': 3456, 'TATAPOWER': 3426, 'TATASTEEL': 3499, 'TCS': 11536, 'TECHM': 13538, 'TITAN': 3506, 'TORNTPHARM': 3518, 'TORNTPOWER': 13786, 'TRENT': 1964, 'TVSMOTOR': 8479, 'UBL': 16713, 'ULTRACEMCO': 11532, 'UPL': 11287, 'VEDL': 3063, 'VOLTAS': 3718, 'WIPRO': 3787, 'ZEEL': 3812}

lickers=[]

# %%
investment=10000
risk=50   
portfolio=30000




ohlcv_database=pd.DataFrame()

order=[]
order1=[]
price=0

position=""
position=""
prise=0
ltp=0



# %%
def selection1():
    global lickers,kickers
    for ticker in kickers:
       
        print('analyzing for:', ticker)
        print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        df=candles(ticker)

        df['8 EMA']=TA.EMA(df,8)
        df['20 EMA']=TA.EMA(df,20)
        for i in range(len(df)):
            if df['Open'][i]<df['8 EMA'] and df['Open'][i]<df['20 EMA'][i]:
                df['condition'][i]=1

            else:
                df['condition'][i]=0

            
        if df['condition'][-2]==1 and (df['Close'][-2]-df['Open'][-2])/(df['High'][-2]-df['Low'][-2])>.9:
            lickers.append(ticker)
        print(df)

 
               
              

        # except Exception as e:
        #     print(e)
        #     bot.sendMessage(1039725953, 'some error occurred')
           


# %%


selection1()
try:
    print(lickers)
    bot.sendMessage(1039725953, lickers)

except:
    print('couldn,t send message')



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
for ticker in yickers:
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

                high[ticker]=df['High'].iloc[-1]

        except Exception as e:
            print(e)
            bot.sendMessage(1039725953, 'some error occurred')
           
      

        


# %%
time.sleep(300-(time.time()-tame))
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
            stock=ticker


    high=high[stock]
    low=0
except:
    print("no stock selected")

bot.sendMessage(1039725953, stock)


# %%
def market_order(instrument,investment,risk):
    global price,order,order1,start_time,stock,order1,ltp,kickers


    price=float(ltp)
    units=round(investment/price,0)
   
    if units>0:
        try:
            orderparams = {
                "variety": "NORMAL",
                "tradingsymbol": str(instrument)+'-EQ',
                "symboltoken": str(kickers[instrument]),
                "transactiontype": "BUY",
                "exchange": "NSE",
                "ordertype": "MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price":str(price),

                "quantity": str(units)
                }
            orderId=obj.placeOrder(orderparams)
            print("The order  is placed for : ", instrument)
            bot.sendMessage(1039725953, 'long position generatted')

        except:
            print("Order placement failed..... some error ")
            bot.sendMessage(1039725953, 'Order placement failed..... some error')


    if units<0:
        try:
            orderparams = {
                "variety": "NORMAL",
                "tradingsymbol": str(instrument)+'-EQ',
                "symboltoken": str(kickers[instrument]),
                "transactiontype": "SELL",
                "exchange": "NSE",
                "ordertype": "MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price":str(price),

                "quantity": str(units)
                }
            orderId=obj.placeOrder(orderparams)
            print("The order  is placed for : ", instrument)
            bot.sendMessage(1039725953, 'short position generated')

        except:
            print("Order placement failed..... some error ")
            bot.sendMessage(1039725953, 'Order placement failed..... some error')
        




    



def market_order1(instrument,investment):
    global price,position,order,ltp,stock

    price=float(ltp)
    units=round(investment/price,0)



    if units>0:
        try:
            orderparams = {
                "variety": "NORMAL",
                "tradingsymbol": str(instrument)+'-EQ',
                "symboltoken": str(kickers[instrument]),
                "transactiontype": "BUY",
                "exchange": "NSE",
                "ordertype": "MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price":str(price),

                "quantity": str(units)
                }
            orderId=obj.placeOrder(orderparams)
            print("The order  is placed for : ", instrument)
            bot.sendMessage(1039725953, 'squarred off')

        except:
            print("Order placement failed..... some error ")
            bot.sendMessage(1039725953, 'Order squareoff failed..... some error')
            





    if units<0:
        try:
            orderparams = {
                "variety": "NORMAL",
                "tradingsymbol": str(instrument)+'-EQ',
                "symboltoken": str(kickers[instrument]),
                "transactiontype": "SELL",
                "exchange": "NSE",
                "ordertype": "MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price":str(price),

                "quantity": str(units)
                }
            orderId=obj.placeOrder(orderparams)
            print("The order  is placed for : ", instrument)
            bot.sendMessage(1039725953, 'squarred off')

        except:
            print("Order placement failed..... some error ")
            bot.sendMessage(1039725953, 'Order squareoff failed..... some error')



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
        timedate=time.localtime(times)
        t=timedate.tm_min%5
        tr=timedate.tm_min-t
        trr=timedate.tm_hour
        time.sleep(.25)
        if position=='long' and str(trr)+':'+str(tr) in df.index[-2]:
            
                
            
            low=df['Low'].iloc[-2]

        if position=='short' and str(trr)+':'+str(tr) in df.index[-2]:
            
            
            high1=df['High'].iloc[-2]




        req_list_=[{"Exch":"N","ExchType":"C","Symbol":stock}]
            
        data=client.fetch_market_feed(req_list_)
        ltp=float(data['Data'][0]['LastRate'])
            



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
        bot.sendMessage(1039725953, 'some error occurred')




# %%

start_time=time.time()

timeout=start_time+60*60*6
bot.sendMessage(1039725953, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
while time.time()<=timeout:
    try:
  
        main()
        print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
   

    except Exception as e:
        print(e)
        bot.sendMessage(1039725953, 'some error occurred')
        



# %%

bot.sendMessage(1039725953, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
bot.sendMessage(1039725953, "squaring off")

req_list_=[{"Exch":"N","ExchType":"C","Symbol":stock}]
    
data=client.fetch_market_feed(req_list_)
ltp=float(data['Data'][0]['LastRate'])        

print("\n \n analyzzing for ",stock)
print(ltp)
if position=="long":
    market_order1(stock,-1*investment)

if position=="short":
    market_order1(stock,investment)     


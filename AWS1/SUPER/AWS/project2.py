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
time.sleep(25)


# %%
import telepot
bot = telepot.Bot('1715056219:AAGxytb3U1gIt1vlVn8Jf5b4za3E1HPuOd4')
bot.getMe()


# %%
def candles(instrument):
    data=yf.download(instrument+'.NS',period='1d',interval='5m')
    return data


# %%
from py5paisa import FivePaisaClient

client = FivePaisaClient(email="sudhanshu8833@gmail.com", passwd="Madhya246###", dob="20010626")
client.login()


# %%
bot.sendMessage(1039725953, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


kickers={'AARTIIND': 7, 'ABFRL': 30108, 'ACC': 22, 'ADANIENT': 25, 'ADANIPORTS': 15083, 'ALKEM': 11703, 'AMARAJABAT': 100, 'AMBUJACEM': 1270, 'APLLTD': 25328, 'APOLLOHOSP': 157, 'APOLLOTYRE': 163, 'ASHOKLEY': 212, 'ASIANPAINT': 236, 'AUBANK': 21238, 'AUROPHARMA': 275, 'AXISBANK': 5900, 'BAJAJ-AUTO': 16669, 'BAJAJFINSV': 16675, 'BAJFINANCE': 317, 'BALKRISIND': 335, 'BANDHANBNK': 2263, 'BANKBARODA': 4668, 'BATAINDIA': 371, 'BEL': 383, 'BERGEPAINT': 404, 'BHARATFORG': 422, 'BHARTIARTL': 10604, 'BHEL': 438, 'BIOCON': 11373, 'BOSCHLTD': 2181, 'BPCL': 526, 'BRITANNIA': 547, 'CADILAHC': 7929, 'CANBK': 10794, 'CHOLAFIN': 685, 'CIPLA': 694, 'COALINDIA': 20374, 'COFORGE': 11543, 'COLPAL': 15141, 'CONCOR': 4749, 'COROMANDEL': 739, 'CUB': 5701, 'CUMMINSIND': 1901, 'DABUR': 772, 'DEEPAKNTR': 19943, 'DIVISLAB': 10940, 'DLF': 14732, 'DRREDDY': 881, 'EICHERMOT': 910, 'ESCORTS': 958, 'EXIDEIND': 676, 'FEDERALBNK': 1023, 'GAIL': 4717, 'GLENMARK': 7406, 'GMRINFRA': 13528, 'GODREJCP': 10099, 'GODREJPROP': 17875, 'GRANULES': 11872, 'GRASIM': 1232, 'GUJGASLTD': 10599, 'HAVELLS': 9819, 'HCLTECH': 7229, 'HDFC': 1330, 'HDFCAMC': 4244, 'HDFCBANK': 1333, 'HDFCLIFE': 467, 'HEROMOTOCO': 1348, 'HINDALCO': 1363, 'HINDPETRO': 1406, 'HINDUNILVR': 1394, 'IBULHSGFIN': 30125, 'ICICIBANK': 4963, 'ICICIGI': 21770, 'ICICIPRULI': 18652, 'IDEA': 14366, 'IDFCFIRSTB': 11184, 'IGL': 11262, 'INDHOTEL': 1512, 'INDIGO': 11195, 'INDUSINDBK': 5258, 'INDUSTOWER': 29135, 'INFY': 1594, 'IOC': 1624, 'IRCTC': 13611, 'ITC': 1660, 'JINDALSTEL': 6733, 'JSWSTEEL': 11723, 'JUBLFOOD': 18096, 'KOTAKBANK': 1922, 'LALPATHLAB':11654, 'LICHSGFIN': 1997, 'LT': 11483, 'LTI': 17818, 'LTTS': 18564, 'LUPIN': 10440,  'MANAPPURAM': 19061, 'MARICO': 4067, 'MARUTI': 10999, 'MCDOWELL-N': 10447, 'METROPOLIS': 9581, 'MFSL': 2142, 'MGL': 17534, 'MINDTREE': 14356, 'MOTHERSUMI': 4204, 'MPHASIS': 4503, 'MRF': 2277, 'MUTHOOTFIN': 23650, 'NAM-INDIA': 357, 'NATIONALUM': 6364, 'NAUKRI': 13751, 'NAVINFLUOR': 14672, 'NESTLEIND': 17963, 'NMDC': 15332, 'NTPC': 11630, 'ONGC': 2475, 'PAGEIND': 14413, 'PEL': 2412, 'PETRONET': 11351, 'PFC': 14299, 'PFIZER': 2643, 'PIDILITIND': 2664, 'PIIND': 24184, 'PNB': 10666, 'POWERGRID': 14977, 'PVR': 13147, 'RAMCOCEM': 2043, 'RBLBANK': 18391, 'RECLTD': 15355, 'RELIANCE': 2885, 'SAIL': 2963, 'SBILIFE': 21808, 'SBIN': 3045, 'SHREECEM': 3103, 'SIEMENS': 3150, 'SRF': 3273, 'SRTRANSFIN': 4306, 'SUNPHARMA': 3351, 'SUNTV': 13404, 'TATACHEM': 3405, 'TATACONSUM': 3432, 'TATAMOTORS': 3456, 'TATAPOWER': 3426, 'TATASTEEL': 3499, 'TCS': 11536, 'TECHM': 13538, 'TITAN': 3506, 'TORNTPHARM': 3518, 'TORNTPOWER': 13786, 'TRENT': 1964, 'TVSMOTOR': 8479, 'UBL': 16713, 'ULTRACEMCO': 11532, 'UPL': 11287, 'VEDL': 3063, 'VOLTAS': 3718, 'WIPRO': 3787, 'ZEEL': 3812}
lickers=[]


# %%
investment=10000
risk=50
profit=100
portfolio=30000




ohlcv_database=pd.DataFrame()



units={}
order={}
position={}
price={}
for ticker in kickers:
    position[ticker]=''
    
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
        condition=[]
        
        for i in range(len(df)):
            if df['Open'][i]<df['8 EMA'][i] and df['Open'][i]<df['20 EMA'][i] and df['Close'][i]>df['8 EMA'][i] and df['Close'][i]>df['20 EMA'][i]:
                condition.append(1)

            else:
                
                condition.append(0)

        

        df['condition']=np.array(condition)
        if df['condition'][-3]==1 and (df['Close'][-3]-df['Open'][-3])/(df['High'][-3]-df['Low'][-3])>.9:
            lickers.append(ticker)
        bot.sendMessage(1039725953, lickers)
    


# %%
yickers=[]

def selection2():
    global lickers,yickers,high,kickers,value,stock,kickers,maximum,position
    
    yickers=[]
    stock='hi'
    maximum=0
    value={}
    for ticker in kickers:
        value[ticker]=0
    for ticker in lickers:
        print('analyzing for: ',ticker)
        df=candles(ticker)
        
        if position[ticker]=="" and df['Close'][-2]>df['Open'][-2]:
            if abs((df['High'][-2]-df['Close'][-2]))>abs((df['Close'][-2]-df['Open'][-2])*2.5):
                yickers.append(ticker)
                value[ticker]=abs(df['High'][-2]-df['Close'][-2])

        elif position[ticker]=="" and df['Close'][-2]<df['Open'][-2]:
            if abs((df['High'][-2]-df['Open'][-2]))>abs((df['Open'][-2]-df['Close'][-2])*2.5):
                yickers.append(ticker)
                value[ticker]=abs(df['High'][-2]-df['Open'][-2])


        for ticker in kickers:
            if value[ticker]>maximum:
                maximum=value[ticker]
                stock=ticker


    

    

        


        
           


# %%
def market_order(instrument,investment,risk):
    global price,position,price_in,portfolio,order,ltp,stock

    req_list_=[{"Exch":"N","ExchType":"C","Symbol":instrument}]
    
        
    data=client.fetch_market_feed(req_list_)
    ltp=float(data['Data'][0]['LastRate'])
    
    
    
    
        
    units=round(investment/ltp,0)

    if units<0:
 
        
        order[instrument]=[]
        order[instrument].append(float(ltp))
        order[instrument].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        position[instrument]="short"
        order[instrument].append("short")
        price[instrument]=float(ltp)

        


    print("order filled for ",instrument)
    bot.sendMessage(1039725953, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    bot.sendMessage(1039725953, 'order made for')
    bot.sendMessage(1039725953, instrument)
    bot.sendMessage(1039725953, '****************')
    stock='hi'

# %%
def market_order1(instrument,investment):
    global price,price1,position,price_out,portfolio,order,ltp,prise



     
    
    units=round(investment/ltp,0)
    

    if units>0:
        
        order[instrument].append(float(ltp[instrument]))
        order[instrument].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        order[instrument]=float(ltp)   
        
        position[instrument]="none"





    
    print("order squared off for ",instrument)
    bot.sendMessage(1039725953, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    bot.sendMessage(1039725953, 'order squared off for')
    bot.sendMessage(1039725953, instrument)
    bot.sendMessage(1039725953, '****************')


# %%

# %%
def trade_signal(instrument,l_s,investment,risk,profit):
    
    global ltp,position,high,low,high1,stock,times,price



    signal=""


    units=investment/price[instrument]
                   
    if l_s=="short":
        if ltp>price[instrument]+ risk/units or ltp<price[instrument]-profit/units:
 
            signal="squareoffbuy"

    return signal    


# %%

# %%
def main():
    global investment,risk,ltp,position,prise,kickers,stock,times,start_time,profit,lickers
    
    
    times=time.time()
    selection1()
    print(lickers)
    
    times1=time.time()

    j=5
    while j>0:


        
        for ticker in kickers:
            if time.time()>=times+150:
                j=2
                break


            if position[ticker]=='short':

                req_list_=[{"Exch":"N","ExchType":"C","Symbol":ticker}]
                    
                data=client.fetch_market_feed(req_list_)
                ltp=float(data['Data'][0]['LastRate'])
                print("shorted stock analyzing", ticker)
                print(ltp)
                signal=trade_signal(ticker, position[ticker],investment,risk,profit)



                if signal=="squareoffbuy":
                    market_order1(ticker,investment)

        if j==2:
            break
        
        


    bot.sendMessage(1039725953, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    bot.sendMessage(1039725953, 'selection 2 started')
    bot.sendMessage(1039725953, '****************************')
    times=time.time()
    selection2()
    bot.sendMessage(1039725953, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    bot.sendMessage(1039725953, 'order making time')
    bot.sendMessage(1039725953, '****************************')

    if stock!='hi' and time.time()<start_time+160+60*60*4:
        market_order(stock,-1*investment,risk)
    
    times1=time.time()
    
    j=5
    while j>0:

        for ticker in kickers:
            if time.time()>=times+149:
                j=2
                break


            if position[ticker]=='short':
                

                req_list_=[{"Exch":"N","ExchType":"C","Symbol":ticker}]
                    
                data=client.fetch_market_feed(req_list_)
                ltp=float(data['Data'][0]['LastRate'])
                print("shorted stock analyzing", ticker)
                print(ltp)

                signal=trade_signal(ticker, position[ticker],investment,risk)
                if signal=="squareoffbuy":
                    market_order1(ticker,investment)
    
        if j==2:
            break
    lickers=[]





start_time=time.time()

timeout=start_time+60*60*5+60*48
bot.sendMessage(1039725953, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
bot.sendMessage(1039725953, 'time for actual start of the bot')
bot.sendMessage(1039725953, '*************************')
while time.time()<=timeout:
  
    try:
        main()
        print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    except Exception as e:
        print(e)
        bot.sendMessage(1039725953, 'bot is running')

        


        


# %%


# %%

bot.sendMessage(1039725953, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

for ticker in kickers:
    req_list_=[{"Exch":"N","ExchType":"C","Symbol":ticker}]
        
    data=client.fetch_market_feed(req_list_)
    ltp=float(data['Data'][0]['LastRate'])        

    print("\n \n analyzzing for ",ticker)
    print(ltp)
    if position=="long":
        market_order1(ticker,-1*investment)

    if position=="short":
        market_order1(ticker,investment)     


# %%





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


df.to_csv("project23.csv")

bot.sendDocument(1039725953, document=open('project23.csv', 'rb'))






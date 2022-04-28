
import pandas as pd
import time
from finta import TA
from smartapi import SmartWebSocket
import numpy as np
import pandas as pd
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import datetime as dt
import copy
import json
from smartapi import SmartConnect 

obj=SmartConnect(api_key="e6IdqcDR")
data = obj.generateSession("S776051","Madhya246###")
refreshToken= data['data']['refreshToken']
feedToken=obj.getfeedToken()
userProfile= obj.getProfile(refreshToken)

FEED_TOKEN= feedToken
CLIENT_CODE="S776051"

ss =SmartWebSocket(FEED_TOKEN, CLIENT_CODE)

tickers=["10940","1394","1660","3045","694","317","11723","3787","13538","3432","3103"]

investment=5000
risk=50   
portfolio=30000
transaction_cost=.0075
price={}
price1={}
position={}
for ticker in tickers:
    price[ticker]=0
    price1[ticker]=0
    position[ticker]=""

ohlcv_database=pd.DataFrame()
stock=[]
profit=[]
price_in=[]
price_out=[]
order=[]
ltp=0

from smartapi import SmartConnect 
obj=SmartConnect(api_key="iJ3YYOXH")
data = obj.generateSession("S776051","Madhya246###")
refreshToken= data['data']['refreshToken']
feedToken=obj.getfeedToken()
userProfile= obj.getProfile(refreshToken)

def candle(instrument):
    ohlc_intraday=pd.DataFrame()

    historicParam={
    "exchange": "NSE",
    "symboltoken": instrument,
    "interval": "FIVE_MINUTE",
    "fromdate": "2021-04-08 09:15", 
    "todate": "2021-06-15 09:30"
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

def MACD(DF,a,b,c):

    df = DF.copy()
    df["MA_Fast"]=df["close"].ewm(span=a,min_periods=a).mean()
    df["MA_Slow"]=df["close"].ewm(span=b,min_periods=b).mean()
    df["MACD"]=df["MA_Fast"]-df["MA_Slow"]
    df["Signal"]=df["MACD"].ewm(span=c,min_periods=c).mean()

    return df

def market_order(instrument,investment,risk):
    global price,position,price_in,portfolio

    price[instrument]=float(ltp)    
    units=round(investment/price[instrument],0)

    price_in.append(price[instrument])
    stock.append(instrument)
    if units>0:
        position[instrument]="long"
        order.append("long")

        portfolio=portfolio-units*price[instrument]

    if units<0:
        position[instrument]="short"
        order.append("short")
        portfolio=portfolio+abs(units*price[instrument])


    print("order filled for ",instrument)

def market_order1(instrument,investment):
    global price,price1,position,price_out,portfolio



    price1[instrument]=float(ltp)    
    units=round(investment/price1[instrument],0)

    price_out.append(price1[instrument])
    if units>0:


            
        position[instrument]=""
        portfolio=portfolio-units*price1[instrument] - .01*abs(price[instrument]-price1[instrument])


    if units<0:
        position[instrument]=""

        portfolio=portfolio+units*price1[instrument] -.01*abs(price[instrument]-price1[instrument]) 


    print("order squared off for ",instrument)

def trade_signal(instrument,l_s):
    
    global ltp
    
    ohlc_dict=pd.DataFrame()
    ohlc_dict=candle(instrument)
    

    ohlc_dict.columns=["open","high","low","close","volume"]
    ohlc_dict["fisher 20"]=TA.FISH(ohlc_dict,20)
    ohlc_dict["fisher 10"]=TA.FISH(ohlc_dict,10)    
    ohlc_dict["RSI 16"]=TA.RSI(ohlc_dict,16)
    ohlc_dict["RSI 21"]=TA.RSI(ohlc_dict,21)
    ohlc_dict["MACD macd line"]=MACD(ohlc_dict,12,26,9)["MACD"]
    ohlc_dict["MACD signal line"]=MACD(ohlc_dict,12,26,9)["Signal"]

    signal=""
    if l_s=="":

        if ohlc_dict["fisher 10"].iloc[-1]>0 and ohlc_dict["fisher 10"].iloc[-2]<0 and ohlc_dict["RSI 16"].iloc[-1]>50: 
            signal="buy"

        elif (ohlc_dict["fisher 20"].iloc[-1]<0 and ohlc_dict["fisher 20"].iloc[-1-1]>0) and ohlc_dict["MACD macd line"].iloc[-1]<ohlc_dict["MACD signal line"].iloc[-1] and ohlc_dict["RSI 21"].iloc[-1]<42.5:
            signal="sell"
                        
      

    elif l_s=="long":
        if (ohlc_dict["fisher 20"].iloc[-1]<0.5 and ohlc_dict["fisher 20"].iloc[-1-1]>0.5) or ltp>=price[instrument]+.02*price[instrument] or ltp<=price[instrument]-.008*price[instrument]:

            signal="squareoffsell"
                    
    elif l_s=="short":
        if (ohlc_dict["fisher 20"].iloc[-1]>-1 and ohlc_dict["fisher 20"].iloc[-1-1]<-1) or (ohlc_dict[ticker].iloc["fisher 20"][-1]>0 and ohlc_dict["fisher 20"].iloc[-1-1]<0) or ltp<=price[instrument]-.02*price[instrument] or ltp>=price[instrument]+.005*price[instrument]:
            

            signal="squareoffbuy"


    return signal          



def main():
    global tickers,investment,risk,ltp,position
    for ticker in tickers:

        var="nse_cm|"
        token=var+ticker
        task="mw" 

        def on_message(ws, message):
            global ltp
            data=format(message)
            data=data.replace("'",'"')
            data=json.loads(data)
            if data[0]["tk"]==ticker:
                ltp=float(data[0]['ltp'])

                ws.close()

           
            
        def on_open(ws):
            # print("on open")
            ss.subscribe(task,token)
            ws.close()


        # Assign the callbacks.
        ss._on_open = on_open
        ss._on_message = on_message


        ss.connect()

        print("\n \n analyzzing for ",ticker)
        print(ltp)


        l_s= position[ticker]
        print(l_s)
        signal=trade_signal(ticker,l_s)
        if signal=="buy":
            market_order(ticker,investment,risk)
            print("New long position initiated for ",ticker)

        elif signal=="sell":
            market_order(ticker,-1*investment,risk)
            print("New short position initiated for ", ticker)

        elif signal=="squareoffbuy":
            market_order1(ticker,investment)

        elif signal=="squareoffsell":
            market_order1(ticker,-1*investment)
        print("###############################")


start_time=time.time()
timeout=start_time+60*60*3
while time.time()<=timeout:
    try:
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@") 
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@") 
        print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        main()
        # print("porfolio: ",portfolio)

        # time.sleep(300-(time.time()-start_time)%300)
        
    except KeyboardInterrupt:
        print("keyboard interuption ....... exiting")

for ticker in tickers:
    if position[ticker]=="long":
        market_order1(ticker,-1*investment)

    if position[ticker]=="short":
        market_order1(ticker,investment)     

ohlcv_database["price_in"]=np.array(price_in)
ohlcv_database["price_out"]=np.array(price_out)
ohlcv_database["order"]=np.array(order)
ohlcv_database["stock"]=np.array(stock)
ohlcv_database.to_csv("database2.csv")
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%


import pandas as pd
import time
from finta import TA
import numpy as np
import pandas as pd
import datetime as dt
import copy
import json
from py5paisa import FivePaisaClient

client = FivePaisaClient(email="sudhanshu8833@gmail.com", passwd="Madhya246###", dob="20010626")
client.login()


# %%
tickers={"7":"AARTIIND","100":"AMARAJABAT","144":"GODREJAG","163":"APOLLOTYRE","212":"ASHOKLEY","220":"IEX","275":"AUROPHAR","277":"GICRE","341":"BALRAMCH","357":"NAM-INDIA","383":"BEL","399":"NIACL","404":"BERGEPAI","419":"BEPL","422":"BHARATFO","425":"KHADIM","467":"HDFCLIFE","477":"BIRLACABLE","509":"MAZDOCK","526":"BPCL","583":"CANFINHO","592":"GRAPHITE","625":"CENTURYT","637":"CHAMBLFERT","676":"EXIDEIND","685":"CHOLAFIN","694":"CIPLA","701":"HEMIPROP","724":"TATACOFF","772":"DABUR","811":"DCMSHRIR","919":"EIHOTEL","981":"EPL","1008":"FACT","1041":"FINPIPE","1076":"ZENSARTECH","1085":"GABRIEL","1139":"GICHSGFIN","1174":"GNFC","1235":"GREAVESCOT","1247":"GSFC","1250":"CASTROLIND"}


# %%
ltp=0
investment=5000
risk=50   
portfolio=30000
transaction_cost=.0075
price={}
price_in=[]

ohlcv_database=pd.DataFrame()
j=0
price_out=[]
order={}


price1={}
position={}
for ticker in tickers:
    price[ticker]=0
    price1[ticker]=0
    position[ticker]=""


# %%
def candle(instrument):
    df=client.historical_data('N','C',instrument,'5m','2021-06-23','2021-06-26')
    return df


# %%
def market_order(instrument,investment,risk):
    global price,position,price_in,portfolio,order
    order[instrument]=[]
    order[instrument].append(float(ltp))
    order[instrument].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    
    price[instrument]=float(ltp)    
    units=round(investment/price[instrument],0)
    

   
    if units>0:
        position[instrument]="long"
        order[instrument].append("long")

        portfolio=portfolio-units*price[instrument]

    elif units<0:
        position[instrument]="short"
        order[instrument].append("short")
        portfolio=portfolio+abs(units*price[instrument])


    print("order filled for ",instrument)


# %%
def market_order1(instrument,investment):
    global price,price1,position,price_out,portfolio,order



    price1[instrument]=float(ltp)    
    order[instrument].append(float(ltp))
    units=round(investment/price1[instrument],0)
    order[instrument].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    if units>0:


            
        position[instrument]="none"
        portfolio=portfolio-units*price1[instrument] 


    if units<0:
        position[instrument]="none"

        portfolio=portfolio+abs(units*price1[instrument]) 

 
    print("order squared off for ",instrument)


# %%
def MACD(DF,a,b,c):

    df = DF.copy()
    df["MA_Fast"]=df["close"].ewm(span=a,min_periods=a).mean()
    df["MA_Slow"]=df["close"].ewm(span=b,min_periods=b).mean()
    df["MACD"]=df["MA_Fast"]-df["MA_Slow"]
    df["Signal"]=df["MACD"].ewm(span=c,min_periods=c).mean()

    return df


# %%
def trade_signal(instrument,l_s):
    
    global ltp,price
    
    ohlc_dict=pd.DataFrame()
    ohlc_dict=candle(instrument)
    
    ohlc_dict.set_index("Datetime",inplace=True)
    ohlc_dict.columns=["open","high","low","close","volume"]
    ohlc_dict["fisher 20"]=TA.FISH(ohlc_dict,20)
    ohlc_dict["fisher 10"]=TA.FISH(ohlc_dict,10)    
    ohlc_dict["RSI 16"]=TA.RSI(ohlc_dict,16)
    ohlc_dict["RSI 21"]=TA.RSI(ohlc_dict,21)
    ohlc_dict["MACD macd line"]=MACD(ohlc_dict,12,26,9)["MACD"]
    ohlc_dict["MACD signal line"]=MACD(ohlc_dict,12,26,9)["Signal"]
    ohlc_dict.rename({"open":"Open","high":"High","low":"Low","close":"Close","volume":"Volume"},inplace=True)
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


# %%
def main():
    global tickers,investment,risk,ltp,position
  
    for ticker in tickers.copy():
        try:
        
            req_list_=[{"Exch":"N","ExchType":"C","Symbol":tickers[ticker]}]
                
            data=client.fetch_market_feed(req_list_)
            ltp=float(data['Data'][0]['LastRate'])        
            if ltp==0:
                tickers.pop(ticker,None)
                continue
            print("\n \n analyzzing for ",tickers[ticker])
            print(ltp)


            l_s= position[ticker]
            print(l_s)
            signal=trade_signal(ticker,l_s)
            if signal=="buy":
                market_order(ticker,investment,risk)
                print("New long position initiated for ",tickers[ticker])

            elif signal=="sell":
                market_order(ticker,-1*investment,risk)
                print("New short position initiated for ", tickers[ticker])

            elif signal=="squareoffbuy":
                market_order1(ticker,investment)

            elif signal=="squareoffsell":
                market_order1(ticker,-1*investment)

        except:
            print("something went wrong ...... moving to next iteration")


# %%
start_time=time.time()
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
timeout=start_time+60*60*5
while time.time()<=timeout:
    try:
    #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@") 
    #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@") 
        print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        main()
        # print("porfolio: ",portfolio)

        # time.sleep(300-(time.time()-start_time)%300)
        
    except KeyboardInterrupt:
        print("keyboard interuption ....... exiting")

for ticker in tickers.copy():
    req_list_=[{"Exch":"N","ExchType":"C","Symbol":tickers[ticker]}]
        
    data=client.fetch_market_feed(req_list_)
    ltp=float(data['Data'][0]['LastRate'])        
    if ltp==0:
        tickers.pop(ticker,None)
        continue
    print("\n \n analyzzing for ",tickers[ticker])
    print(ltp)
    if position[ticker]=="long":
        market_order1(ticker,-1*investment)

    if position[ticker]=="short":
        market_order1(ticker,investment)     



# %%
df=pd.DataFrame(order)
df=df.T
df.columns=["price_in","time_in","type","price_out","time_out"]


df.to_csv("valuefisher.csv")



# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import time
from finta import TA
import numpy as np
import pandas as pd
import datetime as dt
import yfinance as yf
import copy
import json
from py5paisa import FivePaisaClient

client = FivePaisaClient(email="sudhanshu8833@gmail.com", passwd="Madhya246###", dob="20010626")
client.login()
print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

# %%
kickers=['AARTIIND','AMARAJABAT','ANDHRSUGAR','GODREJAGRO','APOLLOTYRE','ASHOKLEY','IEX','AUROPHARMA','BALMLAWRIE','BALRAMCHIN','NAM-INDIA','BEL','BEPL','BHARATFORG','KHADIM','HDFCLIFE','BIRLACABLE','MAZDOCK','BPCL','UTIAMC','GRAPHITE','CENTURYTEX','IGARASHI','CHAMBLFERT','EXIDEIND','CHOLAFIN','CIPLA','SHALBY','TATACOFFEE','COROMANDEL','DABUR','DALMIASUG','DHAMPURSUG','EIDPARRY','EIHOTEL','FACT','FINPIPE','ZENSARTECH','GREAVESCOT','GSFC','AMBUJACEM','HINDALCO','HINDOILEXP','HINDPETRO','HSIL','HINDZINC','BURGERKING','ASTERDM','INDHOTEL','INDIACEM','IOC','ITC','HGINFRA','ITI','KABRAEXTRU','KCP','CUMMINSIND','LIBERTSHOE','LICHSGFIN','M&M','CHENNPETRO','BANDHANBNK','RAILTEL','NOCIL','MIDHANI','ONGC','BCLIND','PHILIPCARB','JUBLINGREA','EASEMYTRIP','RALLIS','LXCHEM','RAYMOND','RIIL','SAIL','ORIENTELEC','JINDALSAW','SBIN','SCI','VEDL','TATACHEM','TATAPOWER','TATACONSUM','TATAMOTORS','TNPETRO','WIPRO','WSTCSTPAPR','ZEEL','NBVENTURES','MARICO','MOTHERSUMI','GAIL','CONCOR','ICICIBANK','JAICORPLTD','CUB','AXISBANK','JINDALSTEL','BSOFT','HCLTECH','GLENMARK','WOCKPHARMA','NRBBEARING','CADILAHC','TVSMOTOR','NETFMID150','CHALET','VRLLOG','GAEL','MSTCLTD','PNCINFRA','GODREJCP','MCDOWELL-N','NIFTYBEES','KRBL','GUJGASLTD','BHARTIARTL','OLECTRA','PONNIERODE','GODREJIND','JSL','IGL','DREDGECORP','UPL','PETRONET','PTC','BIOCON','ZOTA','BANKBEES','CCL','ASTRAMICRO','NTPC','JSWSTEEL','EVEREADY','SHOPERSTOP','WELCORP','JKPAPER','GRANULES','JSLHISAR','SWSOLAR','TRIVENI','NITINSPIN','KEC','M&MFIN','KEI','UTTAMSUGAR','SUNTV','RSYSTEMS','ALLCARGO','ELECON','GEECEE','GATI','VISHWARAJ','DCBBANK','TORNTPOWER','MINDAIND','REDINGTON','PFC','FSL','INDIANB','JKTYRE','IBREALEST','BFUTILITIE','FORTIS','GUJAPOLLO','DLF','SPARC','ASIANTILES','MAHINDCIE','CSBBANK','POWERGRID','DELTACORP','RELIGARE','ADANIPORTS','IRB','NMDC','RAIN','RECLTD','VGUARD','HCG','KIRIINDUS','TATAMTRDVR','AJMERA','SHILPAMED','DLINKINDIA','JSWENERGY','HINDCOPPER','SUVENPHAR','SBICARD','RBLBANK','ICICIPRULI','VBL','MANAPPURAM','LAURUSLABS','GPPL','ASHOKA','COALINDIA','MOIL','AVADHSUGAR','COCHINSHIP','ABCAPITAL','MAXHEALTH','BODALCHEM','VSSL','ROSSELLIND','INDUSTOWER','SCHNEIDER','CANBK','GLOBUSSPR','OIL','AEGISCHEM','HAPPSTMNDS','SUNPHARMA','JUSTDIAL','ORIENTCEM','ABFRL','IBULHSGFIN']

# %%
def candle(instrument):
    df=yf.download(instrument+'.NS',dt.datetime.today()-dt.timedelta(1),dt.datetime.today(),interval='15m')
    return df

def selection():

    global kickers,tickers
    for ticker in kickers:
        try:
            print("analyzzing for: ",ticker)
            high2=1000000
            low2=0
            ohlc_dict=candle(ticker)
            
            high1=ohlc_dict['High'][0]
            low1=ohlc_dict['Low'][0]
            # ohlc_dict.set_index('Datetime',inplace=True)
            for i in range(len(ohlc_dict)):

        
                if ohlc_dict['High'][i]>high1:
                    high2=ohlc_dict['High'][i]
                    break
                






        


            for i in range(len(ohlc_dict)):

                if ohlc_dict['Low'][i]<low1:
                    low2=ohlc_dict['Low'][i]




            j=0
            k=0
            for i in range(len(ohlc_dict)):
                if ohlc_dict['High'][i]>high2:
                    j=1

                if ohlc_dict['Low'][i]<low2:
                    k=1

            if j==1 and k==1:
                tickers.append(ticker)

        except:
            print("some problem....moving to next iteration")

# %%

prise=0
ltp=0
investment=5000
risk=50   
portfolio=30000
transaction_cost=.0075
price={}
price_in=[]
list=[]
ohlcv_database=pd.DataFrame()

price_out=[]
order={}
# %%
tickers=[]
selection()
print(tickers)



price1={}
position={}
for ticker in tickers:
    price[ticker]=0
    price1[ticker]=0
    position[ticker]=""

print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
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


def trade_signal(instrument,l_s):
    
    global ltp,price,tickers,high,low
    
    # ohlc_dict=pd.DataFrame()
    # ohlc_dict=candle(int(instrument))    
    # high=ohlc_dict["High"].iloc[-1]
    # low=ohlc_dict['Low'].iloc[-1]


    signal=""
    if l_s=="":
    
        if ltp>high[str(instrument)]:
            signal="buy"
            

        elif ltp<low[str(instrument)]:
            signal="sell"


                        
      

    elif l_s=="long":
        if ltp<=low[str(instrument)]:

            signal="squareoffsell"
            tickers.remove(instrument)

           
                    
    elif l_s=="short":
        if ltp>= high[str(instrument)]:
            signal="squareoffbuy"
            tickers.remove(instrument)
            


    return signal    


def main():
    global tickers,investment,risk,ltp,position,high,low
    for ticker in tickers.copy():
        try:
        
            req_list_=[{"Exch":"N","ExchType":"C","Symbol":ticker}]
                
            data=client.fetch_market_feed(req_list_)
            ltp=float(data['Data'][0]['LastRate'])        
            if ltp==0:
                tickers.remove(ticker)
                continue
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

        except:
            print("something went wrong ...... moving to next iteration")


# %%
time.sleep(600)
start_time=time.time()
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

timeout=start_time+60*60*6.5
high={}
low={}
for ticker in tickers:
    ohlc_dict=candle(ticker)
    high[ticker]=ohlc_dict['High'].iloc[-2]
    low[ticker]=ohlc_dict['Low'].iloc[-2]

while time.time()<=timeout:
    try:

        print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        main()

        
    except KeyboardInterrupt:
        print("keyboard interuption ....... exiting")

for ticker in tickers.copy():
    req_list_=[{"Exch":"N","ExchType":"C","Symbol":ticker}]
        
    data=client.fetch_market_feed(req_list_)
    ltp=float(data['Data'][0]['LastRate'])        
    if ltp==0:
        tickers.remove(ticker)
        continue
    print("\n \n analyzzing for ",ticker)
    print(ltp)
    if position[ticker]=="long":
        market_order1(ticker,-1*investment)

    if position[ticker]=="short":
        market_order1(ticker,investment)     




df=pd.DataFrame(order)
df=df.T
df.columns=["price_in","time_in","type","price_out","time_out"]
print(portfolio)

df.to_csv("rachna.csv")


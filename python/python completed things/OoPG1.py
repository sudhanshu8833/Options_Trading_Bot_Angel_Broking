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
import yfinance as yf
import datetime as dt
from py5paisa import FivePaisaClient

client = FivePaisaClient(email="sudhanshu8833@gmail.com", passwd="Madhya246###", dob="20010626")
client.login()





# %%
tickers=['AARTIIND','AMARAJABAT','ANDHRSUGAR','GODREJAGRO','APOLLOTYRE','ASHOKLEY','IEX','AUROPHARMA','BALMLAWRIE','BALRAMCHIN','NAM-INDIA','BEL','BEPL','BHARATFORG','KHADIM','HDFCLIFE','BIRLACABLE','MAZDOCK','BPCL','UTIAMC','GRAPHITE','CENTURYTEX','IGARASHI','CHAMBLFERT','EXIDEIND','CHOLAFIN','CIPLA','SHALBY','TATACOFFEE','COROMANDEL','DABUR','DALMIASUG','DHAMPURSUG','EIDPARRY','EIHOTEL','FACT','FINPIPE','ZENSARTECH','GREAVESCOT','GSFC','AMBUJACEM','HINDALCO','HINDOILEXP','HINDPETRO','HSIL','HINDZINC','BURGERKING','ASTERDM','INDHOTEL','INDIACEM','IOC','ITC','HGINFRA','ITI','KABRAEXTRU','KCP','CUMMINSIND','LIBERTSHOE','LICHSGFIN','M&M','CHENNPETRO','BANDHANBNK','RAILTEL','NOCIL','MIDHANI','ONGC','BCLIND','PHILIPCARB','JUBLINGREA','EASEMYTRIP','RALLIS','LXCHEM','RAYMOND','RIIL','SAIL','ORIENTELEC','JINDALSAW','SBIN','SCI','VEDL','TATACHEM','TATAPOWER','TATACONSUM','TATAMOTORS','TNPETRO','WIPRO','WSTCSTPAPR','ZEEL','NBVENTURES','MARICO','MOTHERSUMI','GAIL','CONCOR','ICICIBANK','JAICORPLTD','CUB','AXISBANK','JINDALSTEL','BSOFT','HCLTECH','GLENMARK','WOCKPHARMA','NRBBEARING','CADILAHC','TVSMOTOR','NETFMID150','CHALET','VRLLOG','GAEL','MSTCLTD','PNCINFRA','GODREJCP','MCDOWELL-N','NIFTYBEES','KRBL','GUJGASLTD','BHARTIARTL','OLECTRA','PONNIERODE','GODREJIND','JSL','IGL','DREDGECORP','UPL','PETRONET','PTC','BIOCON','ZOTA','BANKBEES','CCL','ASTRAMICRO','NTPC','JSWSTEEL','EVEREADY','SHOPERSTOP','WELCORP','JKPAPER','GRANULES','JSLHISAR','SWSOLAR','TRIVENI','NITINSPIN','KEC','M&MFIN','KEI','UTTAMSUGAR','SUNTV','RSYSTEMS','ALLCARGO','ELECON','GEECEE','GATI','VISHWARAJ','DCBBANK','TORNTPOWER','MINDAIND','REDINGTON','PFC','FSL','INDIANB','JKTYRE','IBREALEST','BFUTILITIE','FORTIS','GUJAPOLLO','DLF','SPARC','ASIANTILES','MAHINDCIE','CSBBANK','POWERGRID','DELTACORP','RELIGARE','ADANIPORTS','IRB','NMDC','RAIN','RECLTD','VGUARD','HCG','KIRIINDUS','TATAMTRDVR','AJMERA','SHILPAMED','DLINKINDIA','JSWENERGY','HINDCOPPER','SUVENPHAR','SBICARD','RBLBANK','ICICIPRULI','VBL','MANAPPURAM','LAURUSLABS','GPPL','ASHOKA','COALINDIA','MOIL','AVADHSUGAR','COCHINSHIP','ABCAPITAL','MAXHEALTH','BODALCHEM','VSSL','ROSSELLIND','INDUSTOWER','SCHNEIDER','CANBK','GLOBUSSPR','OIL','AEGISCHEM','HAPPSTMNDS','SUNPHARMA','JUSTDIAL','ORIENTCEM','ABFRL','IBULHSGFIN']

prise=0
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
# def candle(instrument):
#     df=client.historical_data('N','C',instrument,'1d','2021-06-20','2021-06-26')
#     return df


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
def trade_signal(instrument,l_s):
    
    global ltp,price,tickers,prise
    
    # ohlc_dict=pd.DataFrame()
    # ohlc_dict=candle(int(instrument))    
    # prise=ohlc_dict["Close"].iloc[-1]


    signal=""
    if l_s=="":
    
        if ((prise-ltp)/prise)*100>2 and  ((prise-ltp)/prise)*100<8:
            signal="buy"
            

        elif ((prise-ltp)/prise)*100<-2 and  ((prise-ltp)/prise)*100>-8:
            signal="sell"

        else:
            tickers.remove(instrument)
                        
      

    elif l_s=="long":
        if ltp>= 0.80*(abs(prise-price[instrument]))+price[instrument] or ltp<=price[instrument]-0.80*(abs(prise-price[instrument])):

            signal="squareoffsell"
            tickers.remove(instrument)

           
                    
    elif l_s=="short":
        if ltp>= (0.80*(abs(prise-price[instrument]))+price[instrument]) or ltp<=(price[instrument]-0.80*(abs(prise-price[instrument]))):
            signal="squareoffbuy"
            tickers.remove(instrument)
            


    return signal    


# %%
def main():
    global tickers,investment,risk,ltp,position,prise
    
    for ticker in tickers.copy():
        try:
            req_list_=[{"Exch":"N","ExchType":"C","Symbol":ticker}]
                
            data=client.fetch_market_feed(req_list_)
            ltp=float(data['Data'][0]['LastRate'])
            prise=float(data['Data'][0]['PClose'])        
            if ltp==0:
                tickers.remove(ticker)
                continue
            if prise==0:
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
            print("something went wrong... moving to next iteration")
        # print("###############################")   


# %%
start_time=time.time()
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
timeout=start_time+60*60*2
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
    req_list_=[{"Exch":"N","ExchType":"C","Symbol":ticker}]
        
    data=client.fetch_market_feed(req_list_)
    ltp=float(data['Data'][0]['LastRate'])        
    if ltp==0:
        tickers.pop(ticker,None)
        continue
    print("\n \n analyzzing for ",ticker)
    print(ltp)
    if position[ticker]=="long":
        market_order1(ticker,-1*investment)

    if position[ticker]=="short":
        market_order1(ticker,investment)     



# %%



# %%
df=pd.DataFrame(order)
df=df.T
df.columns=["price_in","time_in","type","price_out","time_out"]
df["stocks"]=df.index
open=[]
stock=[]
# time.sleep(60)
for i in range(len(df)):
    try:
        ohlc_dict=yf.download(df.index[i]+'.NS',dt.datetime.today()-dt.timedelta(10),dt.datetime.today(),interval='60m')
        open.append(ohlc_dict['Open'].iloc[-3])
   
    except:
        open.append(0)


df["open"]=np.array(open)

profit=[]
for i in range(len(df)):
    if df['type'][i]=='long':
        profit.append(((df['price_out'][i]-df['price_in'][i])/df['price_in'][i])*100)

    elif df['type'][i]=='short':
        profit.append(((df['price_in'][i]-df['price_out'][i])/df['price_out'][i])*100)

df["profit"]=np.array(profit)


df.to_csv("opg.csv")

print(portfolio)
# %%



# %%




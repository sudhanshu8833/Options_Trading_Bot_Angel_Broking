# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# %%
import pandas as pd
import yfinance as yf

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
tickers=['AARTIIND','AMARAJABAT','ANDHRSUGAR','GODREJAGRO','APOLLOTYRE','ASHOKLEY','IEX','AUROPHARMA','BALMLAWRIE','BALRAMCHIN','NAM-INDIA','BEL','BEPL','BHARATFORG','KHADIM','HDFCLIFE','BIRLACABLE','MAZDOCK','BPCL','UTIAMC','GRAPHITE','CENTURYTEX','IGARASHI','CHAMBLFERT','EXIDEIND','CHOLAFIN','CIPLA','SHALBY','TATACOFFEE','COROMANDEL','DABUR','DALMIASUG','DHAMPURSUG','EIDPARRY','EIHOTEL','FACT','FINPIPE','ZENSARTECH','GREAVESCOT','GSFC','AMBUJACEM','HINDALCO','HINDOILEXP','HINDPETRO','HSIL','HINDZINC','BURGERKING','ASTERDM','INDHOTEL','INDIACEM','IOC','ITC','HGINFRA','ITI','KABRAEXTRU','KCP','CUMMINSIND','LIBERTSHOE','LICHSGFIN','M&M','CHENNPETRO','BANDHANBNK','RAILTEL','NOCIL','MIDHANI','ONGC','BCLIND','PHILIPCARB','JUBLINGREA','EASEMYTRIP','RALLIS','LXCHEM','RAYMOND','RIIL','SAIL','ORIENTELEC','JINDALSAW','SBIN','SCI','VEDL','TATACHEM','TATAPOWER','TATACONSUM','TATAMOTORS','TNPETRO','WIPRO','WSTCSTPAPR','ZEEL','NBVENTURES','MARICO','MOTHERSUMI','GAIL','CONCOR','ICICIBANK','JAICORPLTD','CUB','AXISBANK','JINDALSTEL','BSOFT','HCLTECH','GLENMARK','WOCKPHARMA','NRBBEARING','CADILAHC','TVSMOTOR','NETFMID150','CHALET','VRLLOG','GAEL','MSTCLTD','PNCINFRA','GODREJCP','MCDOWELL-N','NIFTYBEES','KRBL','GUJGASLTD','BHARTIARTL','OLECTRA','PONNIERODE','GODREJIND','JSL','IGL','DREDGECORP','UPL','PETRONET','PTC','BIOCON','ZOTA','BANKBEES','CCL','ASTRAMICRO','NTPC','JSWSTEEL','EVEREADY','SHOPERSTOP','WELCORP','JKPAPER','GRANULES','JSLHISAR','SWSOLAR','TRIVENI','NITINSPIN','KEC','M&MFIN','KEI','UTTAMSUGAR','SUNTV','RSYSTEMS','ALLCARGO','ELECON','GEECEE','GATI','VISHWARAJ','DCBBANK','TORNTPOWER','MINDAIND','REDINGTON','PFC','FSL','INDIANB','JKTYRE','IBREALEST','BFUTILITIE','FORTIS','GUJAPOLLO','DLF','SPARC','ASIANTILES','MAHINDCIE','CSBBANK','POWERGRID','DELTACORP','RELIGARE','ADANIPORTS','IRB','NMDC','RAIN','RECLTD','VGUARD','HCG','KIRIINDUS','TATAMTRDVR','AJMERA','SHILPAMED','DLINKINDIA','JSWENERGY','HINDCOPPER','SUVENPHAR','SBICARD','RBLBANK','ICICIPRULI','VBL','MANAPPURAM','LAURUSLABS','GPPL','ASHOKA','COALINDIA','MOIL','AVADHSUGAR','COCHINSHIP','ABCAPITAL','MAXHEALTH','BODALCHEM','VSSL','ROSSELLIND','INDUSTOWER','SCHNEIDER','CANBK','GLOBUSSPR','OIL','AEGISCHEM','HAPPSTMNDS','SUNPHARMA','JUSTDIAL','ORIENTCEM','ABFRL','IBULHSGFIN']


# %%
ltp={}
prise={}
for ticker in tickers:
    ltp[ticker]=1
    prise[ticker]=1


# %%



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
    global price,position,price_in,portfolio,order,ltp,prise
    order[instrument]=[]
    order[instrument].append(float(ltp[instrument]))
    order[instrument].append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    
    price[instrument]=float(ltp[instrument])    
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
    global price,price1,position,price_out,portfolio,order,ltp,prise



    price1[instrument]=float(ltp[instrument])    
    order[instrument].append(float(ltp[instrument]))
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
    
        if ((prise[instrument]-ltp[instrument])/prise[instrument])*100>2 and  ((prise[instrument]-ltp[instrument])/prise[instrument])*100<8:
            signal="buy"
            

        elif ((prise[instrument]-ltp[instrument])/prise[instrument])*100<-2 and  ((prise[instrument]-ltp[instrument])/prise[instrument])*100>-8:
            signal="sell"

        # else:
        #     tickers.remove(instrument)
        #     ltp.pop(instrument,None)
        #     prise.pop(instrument,None)                        
      

    elif l_s=="long":
        if ltp[instrument]>= 0.80*(abs(prise[instrument]-price[instrument]))+price[instrument] or ltp[instrument]<=price[instrument]-0.80*(abs(prise[instrument]-price[instrument])):

            signal="squareoffsell"
            # tickers.remove(instrument)
            # ltp.pop(instrument,None)
            # prise.pop(instrument,None)

           
                    
    elif l_s=="short":
        if ltp[instrument]>= (0.80*(abs(prise[instrument]-price[instrument]))+price[instrument]) or ltp[instrument]<=(price[instrument]-0.80*(abs(prise[instrument]-price[instrument]))):
            signal="squareoffbuy"
            # tickers.remove(instrument)
            # ltp.pop(instrument,None)
            # prise.pop(instrument,None)
            


    return signal    


# %%
def main():
    global tickers,investment,risk,ltp,position,prise
    
    for i in range(4):

        req_list_=[{"Exch":"N","ExchType":"C","Symbol":tickers[0+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[1+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[2+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[3+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[4+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[5+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[6+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[7+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[8+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[9+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[10+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[11+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[12+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[13+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[14+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[15+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[16+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[17+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[18+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[19+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[20+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[21+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[22+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[23+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[24+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[25+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[26+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[27+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[28+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[29+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[30+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[31+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[32+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[33+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[34+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[35+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[36+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[37+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[38+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[39+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[40+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[41+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[42+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[43+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[44+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[45+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[46+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[47+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[48+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[49+i]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[49+i]}
                ]
                    
                    
        data=client.fetch_market_feed(req_list_)
        # print(data)
        # print(data)
        j=0
        for ticker in tickers[50*i:50*i+49]:
            ltp[ticker]=float(data['Data'][j]['LastRate'])
            prise[ticker]=float(data['Data'][j]['PClose'])
            print(ticker)
            print(ltp[ticker])
            # # print"(****************)"
            # print(prise[ticker])
            j+=1



        
        for ticker in tickers[50*i:50*i+49]:

            if ltp[ticker]==0:
                tickers.remove(ticker)
                ltp.pop(ticker,None)
                prise.pop(ticker,None)
                print("dvgbhnjmxdcfgvhbnjdcvghbjnmdcgvhb jnmdctvgbhnjdcvgbh")
                
            if prise==0:
                tickers.remove(ticker)
                prise.pop(ticker,None)
                ltp.pop(ticker,None)
                print("dvgbhnjmxdcfgvhbnjdcvghbjnmdcgvhb jnmdctvgbhnjdcvgbh")
                
        # print("\n \n analyzzing for ",ticker)
        # print(ltp)

        for ticker in tickers[50*i:50*i+49]:
            if ltp[ticker]==0:
                continue
            if prise[ticker]==0:
                continue
            print("\n \n analyzzing for ",ticker)
            print(ltp[ticker])
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
    # except:
    #         print("something went wrong... moving to next iteration")
    # print("###############################")   


# %%


# %%




# %%
start_time=time.time()
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
timeout=start_time+30
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


ltp['AARTIND']




# %%




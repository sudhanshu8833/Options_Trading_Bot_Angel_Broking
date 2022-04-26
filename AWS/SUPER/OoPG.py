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

import telepot
bot = telepot.Bot('1946014673:AAGIeqXxBgx4E6Jj5uvTJHxeU0u7f17KWNE')
bot.getMe()
# %%
tickers=['ALEMBICLTD','CHEMCON','GICRE','ANGELBRKG','NIACL','BERGEPAINT','CANFINHOME','CENTENKA','CESC','HEMIPROP','CLNINDIA','DCMSHRIRAM','ELGIEQUIP','EPL','FINCABLES','GABRIEL','GHCL','GICHSGFIN','NEWGEN','GNFC','FMGOETZE','KANSAINER','CASTROLIND','GUJALKALI','HARRMALAYA','HIMATSEIDE','INDIAGLYCO','BECTORFOOD','JAYSREETEA','JINDALPOLY','KANPRPLA','KAKATCEM','KALPATPOWR','ACRYSIL','KOPRAN','TRENT','MAHSEAMLES','STOVEKRAFT','BDL','MUNJALSHOW','HEIDELBERG','NELCO','ISEC','HERANBA','PRSMJOHNSN','RSWM','ANURAS','HITECH','SURYODAY','WONDERLA','BARBEQUE','LODHA','JTEKTINDIA','STARPAPER','SURYAROSNI','TINPLATE','TIRUMALCHM','UNIVCABLES','JUBLPHARMA','VIPIND','VLSFINANCE','WATERBASE','RITES','ZODIACLOTH','ZUARIGLOB','CAPLIPOINT','TNPL','GREENPLY','JAYAGROGN','PANACEABIO','STERTOOLS','JAGSNPHARM','CREDITACC','JMCPROJECT','AARTIDRUGS','RAMCOIND','HERITGFOOD','INDSWFTLAB','FDC','CIGNITITEC','TRIGYN','GRSE','CYIENT','KOTAKBKETF','INTELLECT','CYBERTECH','GOODLUCK','CAMLINFINE','DTIL','SONATSOFTW','SETFNIFBK','STAR','RAJESHEXPO','RAMCOSYS','GEPIL','AVANTIFEED','ARVINDFASN','STLTECH','TAJGVK','HIKAL','KPITTECH','SMARTLINK','SETFNIF50','SYNGENE','PPL','SHARDAMOTR','TCI','SHREEPUSHK','STCINDIA','RADICO','NATHBIOGEN','CREATIVE','SHK','TVTODAY','VAIBHAVGBL','DATAMATICS','NIITLTD','WESTLIFE','LINCOLN','GUFICBIO','WELENT','JBMA','INDOCO','SUPRAJIT','GOKEX','MANGALAM','NH','MANINDS','ICIL','QUICKHEAL','GSPL','INOXLEISUR','INDOTECH','JKLAKSHMI','EMAMILTD','ACE','SELAN','GESHIP','SOBHA','VENUSREM','BANCOINDIA','PLASTIBLEN','JASH','SANGHVIMOV','PITTIENG','SEQUENT','NAHARSPING','KIRLFER','NCLIND','ALPHAGEO','MOTILALOFS','KSCL','KOLTEPATIL','JYOTHYLAB','BRIGADE','ARIES','DVL','JKIL','ONMOBILE','KNRCON','DHANI','PRINCEPIPE','GET&D','UJJIVAN','CROMPTON','SUMICHEM','PARAGMILK','BLS','MHRIL','SUNTECK','POKARNA','REFEX','DBCORP','TRF','ADVENZYMES','DBL','LGBBROSLTD','VERTOZ','KSL','BLISSGVS','HISARMETAL','BOROLTD','BAJAJCON','BSE','SASTASUNDR','CAREERP','RAMKY','WABAG','CLEDUCATE','OBEROIRLTY','PRESTIGE','IOLCP','GRAVITA','KIRLOSENG','STARCEMENT','BFINVEST','ERIS','CDSL','STEL','APEX','DCAL','CAPACITE','ICICITECH','N100','ESTER','ASHIANA','APLLTD','TRITURBINE','POLYMED','RUPA','MINDACORP','SWANENERGY','KITEX','ZUARI','CARERATING','REPCOHOME','ORIENTREF','APTECHT','PREMEXPLN']
ltp={}
prise={}
for ticker in tickers:
    ltp[ticker]=1
    prise[ticker]=1
# %%

bot.sendMessage(1039725953,"hi how are you")

# %%
investment=5000
risk=50   
portfolio=30000
transaction_cost=.0075




order={}

price={}
price1={}
position={}
for ticker in tickers:
    price[ticker]=0
    price1[ticker]=0
    position[ticker]=""


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
# %%
def trade_signal(instrument,l_s):
    
    global ltp,price,tickers,prise,position
    
    # ohlc_dict=pd.DataFrame()
    # ohlc_dict=candle(int(instrument))    
    # prise=ohlc_dict["Close"].iloc[-1]


    signal=""
    if l_s=="":
    
        if ((prise[instrument]-ltp[instrument])/prise[instrument])*100>2 and  ((prise[instrument]-ltp[instrument])/prise[instrument])*100<8:
            signal="buy"
            

        elif ((prise[instrument]-ltp[instrument])/prise[instrument])*100<-2 and  ((prise[instrument]-ltp[instrument])/prise[instrument])*100>-8:
            signal="sell"

        else:
        #     tickers.remove(instrument)
        #     ltp.pop(instrument,None)
        #     prise.pop(instrument,None)                        
            position[instrument]='none'

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
    
    for i in range(3):

        req_list_=[{"Exch":"N","ExchType":"C","Symbol":tickers[0+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[1+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[2+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[3+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[4+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[5+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[6+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[7+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[8+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[9+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[10+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[11+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[12+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[13+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[14+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[15+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[16+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[17+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[18+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[19+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[20+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[21+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[22+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[23+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[24+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[25+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[26+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[27+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[28+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[29+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[30+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[31+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[32+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[33+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[34+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[35+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[36+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[37+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[38+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[39+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[40+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[41+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[42+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[43+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[44+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[45+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[46+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[47+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[48+i*50]},
                {"Exch":"N","ExchType":"C","Symbol":tickers[49+i*50]}
    
                ]
                    
                    
        data=client.fetch_market_feed(req_list_)
        # print(data)
        # print(data)
        j=0
        for ticker in tickers[50*i:50*i+49]:
            ltp[ticker]=float(data['Data'][j]['LastRate'])
            prise[ticker]=float(data['Data'][j]['PClose'])

            j+=1





        for ticker in tickers[50*i:50*i+49]:
            if position[ticker]=='none':
                continue
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
            
            # else:
            #     position[ticker='none']
    # except:
    #         print("something went wrong... moving to next iteration")
    # print("###############################")   





# %%
time.sleep(57)
start_time=time.time()
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

timeout=start_time+60*60*2
while time.time()<=timeout:
    try:
    #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@") 
    #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@") 
        # print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        main()
        print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        # print("porfolio: ",portfolio)

        # time.sleep(300-(time.time()-start_time)%300)
        
    except KeyboardInterrupt:
        print("keyboard interuption ....... exiting")

for ticker in tickers.copy():
    # req_list_=[{"Exch":"N","ExchType":"C","Symbol":ticker}]
        
    # data=client.fetch_market_feed(req_list_)
    # ltp=float(data['Data'][0]['LastRate'])        
    # if ltp==0:
    #     tickers.pop(ticker,None)
    #     continue
    # print("\n \n analyzzing for ",ticker)
    # print(ltp)
    if position[ticker]=="long":
        market_order1(ticker,-1*investment)

    if position[ticker]=="short":
        market_order1(ticker,investment)     



# %%
df=pd.DataFrame(order)
df=df.T
df.columns=["price_in","time_in","type","price_out","time_out"]
df["stocks"]=df.index
open=[]
stock=[]
close=[]

# time.sleep(60)
for i in range(len(df)):
    try:
        ohlc_dict=yf.download(df.index[i]+'.NS',dt.datetime.today()-dt.timedelta(10),dt.datetime.today(),interval='60m')
        open.append(ohlc_dict['Open'].iloc[-3])
        close.append(ohlc_dict['Close'].iloc[-4])


    except:
        open.append(0)


df["open"]=np.array(open)
df['last day Close']=np.array(close)

profit=[]
for i in range(len(df)):
    if df['type'][i]=='long':
        profit.append(((df['price_out'][i]-df['price_in'][i])/df['price_in'][i])*100)

    elif df['type'][i]=='short':
        profit.append(((df['price_in'][i]-df['price_out'][i])/df['price_out'][i])*100)

df["profit"]=np.array(profit)
df.to_csv("opg.csv")






bot.sendDocument(1039725953, document=open('opg.csv', 'rb'))







# %%














# %%

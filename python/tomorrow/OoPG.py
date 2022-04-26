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
kickers={"7":"AARTIIND","100":"AMARAJABAT","144":"GODREJAG","163":"APOLLOTYRE","212":"ASHOKLEY","220":"IEX","275":"AUROPHAR","277":"GICRE","341":"BALRAMCH","357":"NAM-INDIA","383":"BEL","399":"NIACL","404":"BERGEPAI","419":"BEPL","422":"BHARATFO","425":"KHADIM","467":"HDFCLIFE","477":"BIRLACABLE","509":"MAZDOCK","526":"BPCL","583":"CANFINHO","592":"GRAPHITE","625":"CENTURYT","637":"CHAMBLFERT","676":"EXIDEIND","685":"CHOLAFIN","694":"CIPLA","701":"HEMIPROP","724":"TATACOFF","772":"DABUR","811":"DCMSHRIR","919":"EIHOTEL","981":"EPL","1008":"FACT","1041":"FINPIPE","1076":"ZENSARTECH","1085":"GABRIEL","1139":"GICHSGFIN","1174":"GNFC","1235":"GREAVESCOT","1247":"GSFC","1250":"CASTROLIND","1270":"AMBUJACEM","1313":"HARRMALAYA","1360":"HIMATSEIDE","1363":"HINDALCO","1403":"HINDOILEXP","1406":"HINDPETRO","1424":"HINDZINC","1494":"BURGERKING","1508":"ASTERDM","1512":"INDHOTEL","1515":"INDIACEM","1624":"IOC","1660":"ITC","1675":"ITI","1708":"JAYBARMARU","1841":"KCP","1901":"CUMMINSIND","1997":"LICHSGFIN","2031":"M&M","2049":"CHENNPETRO","2263":"BANDHANBNK","2275":"IRISDOREME","2307":"MUNJALSHOW","2431":"RAILTEL","2442":"NOCIL","2463":"MIDHANI","2475":"ONGC","2649":"PHILIPCARB","2783":"JUBLINGREA","2792":"EASEMYTRIP","2816":"RALLIS","2841":"LXCHEM","2859":"RAYMOND","2912":"RIIL","2963":"SAIL","3024":"JINDALSAW","3045":"SBIN","3048":"SCI","3063":"VEDL","3066":"SESHAPAPER","3291":"STARPAPER","3375":"SURYAROSNI","3405":"TATACHEM","3426":"TATAPOWER","3432":"TATACONSUM","3456":"TATAMOTORS","3496":"TIRUMALCHM","3761":"RITES","3787":"WIPRO","3799":"WSTCSTPAPR","3812":"ZEEL","3980":"TNPL","4014":"NBVENTURES","4055":"PANACEABIO","4067":"MARICO","4204":"MOTHERSUMI","4299":"STERTOOLS","4469":"ELECTHERM","4717":"GAIL","4749":"CONCOR","4963":"ICICIBANK","5142":"CIGNITITEC","5143":"JAICORPLTD","5258":"INDUSINDBK","5701":"CUB","5900":"AXISBANK","6733":"JINDALSTEL","6994":"BSOFT","7229":"HCLTECH","7406":"GLENMARK","7862":"GEPIL","7929":"CADILAHC","7936":"AVANTIFEED","8479":"TVSMOTOR","9309":"STLTECH","9668":"HIKAL","9683":"KPITTECH","10099":"GODREJCP","10447":"MCDOWELL-N","10576":"NIFTYBEES","10577":"KRBL","10599":"GUJGASLTD","10604":"BHARTIARTL","10637":"OLECTRA","10990":"RADICO","11037":"ICICIBANKN","11155":"CREATIVE","11212":"SHK","11236":"JSL","11262":"IGL","11265":"TVSELECT","11271":"DREDGECORP","11287":"UPL","11351":"PETRONET","11355":"PTC","11373":"BIOCON","11394":"ZOTA","11423":"DATAMATICS","11439":"BANKBEES","11522":"NIITLTD","11618":"ASTRAMICRO","11626":"WELENT","11630":"NTPC","11723":"JSWSTEEL","11778":"GOKEX","11821":"WELCORP","11840":"NH","11860":"JKPAPER","11872":"GRANULES","12304":"JSLHISAR","12489":"SWSOLAR","13081":"TRIVENI","13116":"QUICKHEAL","13197":"GSPL","13221":"INOXLEISUR","13260":"KEC","13285":"M&MFIN","13404":"SUNTV","13501":"ALLCARGO","13517":"EMAMILTD","13587":"ACE","13643":"ELECON","13688":"GATI","13725":"DCBBANK","13786":"TORNTPOWER","14096":"SIYSIL","14134":"PITTIENG","14255":"REDINGTON","14296":"SEQUENT","14299":"PFC","14304":"FSL","14309":"INDIANB","14435":"JKTYRE","14450":"IBREALEST","14490":"NCLIND","14567":"BFUTILITIE","14582":"SRHHYPOLTD","14592":"FORTIS","14732":"DLF","14788":"SPARC","14889":"ASIANTILES","14937":"MAHINDCIE","14977":"POWERGRID","15044":"DELTACORP","15068":"RELIGARE","15083":"ADANIPORTS","15184":"BRIGADE","15313":"IRB","15332":"NMDC","15337":"RAIN","15355":"RECLTD","15362":"VGUARD","16639":"KIRIINDUS","16965":"TATAMTRDVR","17069":"UJJIVAN","17094":"CROMPTON","17105":"SUMICHEM","17333":"MHRIL","17641":"SUNTECK","17651":"POKARNA","17752":"SHILPAMED","17851":"DLINKINDIA","17869":"JSWENERGY","17881":"DBCORP","17939":"HINDCOPPER","17971":"SBICARD","18321":"LGBBROSLTD","18391":"RBLBANK","18652":"ICICIPRULI","19061":"MANAPPURAM","19234":"LAURUSLABS","19235":"IMFA","19731":"GPPL","20188":"WABAG","20302":"PRESTIGE","20374":"COALINDIA","20534":"GRAVITA","20830":"MOIL","21174":"CDSL","21614":"ABCAPITAL","21704":"DCAL","22377":"MAXHEALTH","22739":"N100","25017":"BODALCHEM","25584":"TRITURBINE","25724":"RUPA","29113":"CARERATING","29135":"INDUSTOWER","31163":"ORIENTREF","31234":"SCHNEIDER","10794":"CANBK","17424":"GLOBUSSPR","17438":"OIL","48":"HAPPSTMNDS","3351":"SUNPHARMA","30089":"ORIENTCEM","30108":"ABFRL","30125":"IBULHSGFIN"}

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
            tickers.pop(instrument,None)
                        
      

    elif l_s=="long":
        if ltp>= 0.80*(abs(prise-price[instrument]))+price[instrument] or ltp<=price[instrument]-0.80*(abs(prise-price[instrument])):

            signal="squareoffsell"
            tickers.pop(instrument,None)

           
                    
    elif l_s=="short":
        if ltp>= (0.80*(abs(prise-price[instrument]))+price[instrument]) or ltp<=(price[instrument]-0.80*(abs(prise-price[instrument]))):
            signal="squareoffbuy"
            tickers.pop(instrument,None)
            


    return signal    


# %%
def main():
    global tickers,investment,risk,ltp,position,prise
    
    for ticker in tickers.copy():
        try:
            req_list_=[{"Exch":"N","ExchType":"C","Symbol":tickers[ticker]}]
                
            data=client.fetch_market_feed(req_list_)
            ltp=float(data['Data'][0]['LastRate'])
            prise=float(data['Data'][0]['PClose'])        
            if ltp==0:
                tickers.pop(ticker,None)
                continue
            if prise==0:
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
            print("something went wrong... moving to next iteration")
        # print("###############################")   


# %%
start_time=time.time()
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
timeout=start_time+12
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
        ohlc_dict=yf.download(+'.NS',dt.datetime.today()-dt.timedelta(10),dt.datetime.today(),interval='60m')
        open.append(ohlc_dict['Open'].iloc[-3])
        stock.append(tickers[ticker])
    except:
        open.append(0)
        stock.append(tickers[ticker])

df["open"]=np.array(open)
df['stoc']=np.array(stock)
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




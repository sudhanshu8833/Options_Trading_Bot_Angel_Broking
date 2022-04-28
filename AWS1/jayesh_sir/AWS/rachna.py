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
print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
client = FivePaisaClient(email="sudhanshu8833@gmail.com", passwd="Madhya246###", dob="20010626")
client.login()


# %%
kickers=['AARTIIND','ABB','ALEMBICLTD','AMARAJABAT','ROUTE','ANDHRSUGAR','GODREJAGRO','APCOTEXIND','APOLLOHOSP','APOLLOTYRE','UNIDT','ASHOKLEY','IEX','ASIANPAINT','CHEMCON','AUROPHARMA','GICRE','TIINDIA','BAJFINANCE','ANGELBRKG','BALKRISIND','BALMLAWRIE','BALRAMCHIN','CAMS','NAM-INDIA','BATAINDIA','BBTC','BEL','MAHLOG','BEML','NIACL','BERGEPAINT','BEPL','BHARATFORG','KHADIM','BHARATGEAR','IFGLEXPOR','HDFCLIFE','BIRLACABLE','BIRLACORPN','MAZDOCK','BPCL','UTIAMC','BRITANNIA','LIKHITHA','CANFINHOME','GRAPHITE','CARBORUNIV','CENTENKA','CENTURYTEX','CESC','IGARASHI','CHAMBLFERT','EXIDEIND','CHOLAFIN','CIPLA','HEMIPROP','SHALBY','CLNINDIA','TATACOFFEE','COROMANDEL','COSMOFILMS','FSC','CRISIL','DABUR','DALMIASUG','DCMSHRIRAM','DEEPAKFERT','DHAMPURSUG','DRREDDY','EICHERMOT','EIDPARRY','EIHOTEL','ELGIEQUIP','ESCORTS','EPL','EVERESTIND','FACT','FINCABLES','FINPIPE','UFLEX','ZENSARTECH','GABRIEL','GHCL','APOLLO','GICHSGFIN','NEWGEN','GMBREW','GNFC','GODFRYPHLP','AMBER','GLAND','FMGOETZE','KANSAINER','GRASIM','GREAVESCOT','GSFC','CASTROLIND','GUJALKALI','AMBUJACEM','HARRMALAYA','HDFC','HDFCBANK','HEG','HEROMOTOCO','HIMATSEIDE','HINDALCO','HINDUNILVR','HINDOILEXP','HINDPETRO','HSIL','HINDZINC','IFBIND','BURGERKING','ASTERDM','INDHOTEL','INDIACEM','INDIAGLYCO','INDIANHUME','GMMPFAUDLR','INFY','INGERRAND','IOC','BECTORFOOD','IPCALAB','ITC','HGINFRA','ITI','JAYBARMARU','JAYSREETEA','JBCHEPHARM','JINDALPOLY','KANPRPLA','AWHCL','KABRAEXTRU','KAJARIACER','KAKATCEM','KALPATPOWR','KCP','ACRYSIL','CUMMINSIND','KOPRAN','KOTAKBANK','TRENT','LIBERTSHOE','LICHSGFIN','M&M','RAMCOCEM','CHENNPETRO','HOMEFIRST','VTL','MAHSEAMLES','STOVEKRAFT','MASTEK','MFSL','BDL','BANDHANBNK','HAL','BESTAGRO','MUNJALSHOW','HEIDELBERG','NELCO','SANDHAR','PEL','RAILTEL','NOCIL','MIDHANI','ONGC','ISEC','BCLIND','HUHTAMAKI','HERANBA','PHILIPCARB','PIDILITIND','POLYPLEX','MTARTECH','PRSMJOHNSN','JUBLINGREA','EASEMYTRIP','RSWM','RALLIS','ANURAS','LXCHEM','RANEHOLDIN','RAYMOND','RELIANCE','RIIL','SAIL','SURYODAY','ORIENTELEC','NAZARA','WONDERLA','JINDALSAW','SBIN','SCI','VEDL','SESHAPAPER','INDOSTAR','SHREYANIND','BARBEQUE','SHREYAS','SIEMENS','LODHA','JTEKTINDIA','SRF','TEMBO','STARPAPER','SUPREMEIND','SURYAROSNI','TATACHEM','TATAELXSI','TATAMETALI','TATAPOWER','TATACONSUM','TATAMOTORS','TINPLATE','TIRUMALCHM','TATASTEEL','TITAN','TNPETRO','TORNTPHARM','UNIVCABLES','JUBLPHARMA','SOLARA','VIPIND','VLSFINANCE','VOLTAS','TATACOMM','WATERBASE','VENKEYS','RITES','WIPRO','WSTCSTPAPR','ZEEL','ZODIACLOTH','ZUARIGLOB','VARROC','SOMANYCERA','CAPLIPOINT','NATCOPHARM','TNPL','GREENPLY','NBVENTURES','JAYAGROGN','PANACEABIO','MARICO','TCNSBRANDS','MOTHERSUMI','HDFCAMC','SRTRANSFIN','JAGSNPHARM','CREDITACC','JMCPROJECT','ELECTHERM','AARTIDRUGS','MPHASIS','RAMCOIND','HERITGFOOD','GAIL','CONCOR','INDSWFTLAB','FDC','ICICIBANK','SHARDACROP','CIGNITITEC','JAICORPLTD','INDUSINDBK','ASAHIINDIA','TRIGYN','GRSE','CUB','CYIENT','KOTAKBKETF','AXISBANK','INTELLECT','MONTECARLO','CYBERTECH','GOODLUCK','CAMLINFINE','GULPOLY','TECHNOE','SONATSOFTW','JINDALSTEL','BSOFT','ACCELYA','HCLTECH','STAR','RAJESHEXPO','GLENMARK','WOCKPHARMA','NRBBEARING','RAMCOSYS','GEPIL','CADILAHC','AVANTIFEED','DALBHARAT','RPSGVENT','BLUESTARCO','TVSMOTOR','NETFMID150','CHALET','VRLLOG','GAEL','NOVARTIND','ANUP','ARVINDFASN','STLTECH','TAJGVK','MSTCLTD','PNCINFRA','METROPOLIS','POLYCAB','HIKAL','KPITTECH','HAVELLS','SMARTLINK','EMAMIPAP','GODREJCP','SETFNIF50','SYNGENE','PPL','LUPIN','MCDOWELL-N','ARVSMART','SHARDAMOTR','NIFTYBEES','KRBL','TCI','SHREEPUSHK','GUJGASLTD','BHARTIARTL','OLECTRA','GODREJIND','DIVISLAB','STCINDIA','RADICO','MARUTI','LIQUIDBEES','DCMNVL','NATHBIOGEN','CREATIVE','INDIGO','SHK','JSL','IGL','TVSELECT','DREDGECORP','TVTODAY','UPL','LUXIND','PETRONET','PTC','VAIBHAVGBL','BIOCON','ZOTA','SALZERELEC','RKFORGE','DATAMATICS','SPANDANA','BANKBEES','CCL','LT','APARINDS','NIITLTD','ULTRACEMCO','TCS','COFORGE','WESTLIFE','LINCOLN','GUFICBIO','ASTRAMICRO','WELENT','NTPC','LALPATHLAB','INDOCO','SUPRAJIT','ALKEM','JSWSTEEL','GDL','GOKEX','EVEREADY','SHOPERSTOP','MANGALAM','WELCORP','NH','JKPAPER','GRANULES','MANINDS','GOLDIAM','ICIL','AURIONPRO','JSLHISAR','SWSOLAR','SORILINFRA','TRIVENI','VIMTALABS','QUICKHEAL','PVR','NITINSPIN','ENIL','GSPL','INOXLEISUR','KEC','M&MFIN','CENTURYPLY','KEI','SOLARINDS','UTTAMSUGAR','BHAGERIA','SUNTV','GPIL','RSYSTEMS','KAMDHENU','JKLAKSHMI','ALLCARGO','EMAMILTD','VIDHIING','TECHM','GRINDWELL','ACE','SELAN','IRCTC','ELECON','TALBROAUTO','GEECEE','GATI','VISHWARAJ','DCBBANK','FLUOROCHEM','NAUKRI','GESHIP','TORNTPOWER','SOBHA','JINDRILL','BANCOINDIA','HIRECT','LUMAXTECH','SANGHVIMOV','SAGCEM','IGPL','SIYSIL','PITTIENG','MINDAIND','REDINGTON','SEQUENT','PFC','FSL','INDIANB','SMSPHARMA','MINDTREE','ASTRAL','LAOPALA','JKTYRE','NAHARSPING','NAHARPOLY','IBREALEST','KIRLFER','NCLIND','BALAMINES','PHOENIXLTD','BFUTILITIE','FORTIS','INSECTICID','NAVINFLUOR','GOACARBON','DLF','SPARC','DECCANCE','ASIANTILES','SRIPIPES','MAHINDCIE','MOTILALOFS','CSBBANK','KSCL','POWERGRID','MAANALU','BAJAJELEC','DELTACORP','RELIGARE','ADANIPORTS','KOLTEPATIL','COLPAL','JYOTHYLAB','BRIGADE','ARIES','DVL','CEATLTD','JKIL','ONMOBILE','KNRCON','HERCULES','IRB','NMDC','RAIN','SHALPAINTS','RECLTD','VGUARD','DHANI','NESCO','HCG','PRINCEPIPE','KIRIINDUS','BAJAJ-AUTO','BAJAJFINSV','UBL','GET&D','VINYLINDIA','TATAMTRDVR','RUCHI','THYROCARE','UJJIVAN','CROMPTON','SUMICHEM','PARAGMILK','BLS','AJMERA','MHRIL','ASALCBR','MAHEPC','SUNTECK','POKARNA','QUESS','SHILPAMED','SARDAEN','REFEX','LTI','DLINKINDIA','JSWENERGY','GODREJPROP','DBCORP','HINDCOPPER','SUVENPHAR','SBICARD','TRF','WHIRLPOOL','ADVENZYMES','DBL','JUBLFOOD','SPAL','LGBBROSLTD','PERSISTENT','RBLBANK','CUPID','LTTS','GNA','ICICIPRULI','ENDURANCE','VERTOZ','KSL','PNBHOUSING','VBL','MANAPPURAM','KIOCL','TCIEXP','LAURUSLABS','IMFA','BLISSGVS','DFMFOODS','ITDC','BOROLTD','ROSSARI','BAJAJCON','BSE','GPPL','DMART','DEEPAKNTR','SASTASUNDR','CAREERP','RAMKY','CANTABIL','AKSHARCHEM','ASHOKA','WABAG','OBEROIRLTY','PRESTIGE','SHANKARA','RESPONIND','CGCL','COALINDIA','IOLCP','APCL','GRAVITA','DOLLAR','SUPERHOUSE','SCHAND','MOIL','PSPPROJECT','KIRLOSENG','STARCEMENT','BFINVEST','ERIS','CDSL','GTPL','AUBANK','ICICILOVOL','SALASAR','MAGADSUGAR','AVADHSUGAR','SIS','COCHINSHIP','ABCAPITAL','APEX','DIXON','DCAL','CHOLAHLDNG','CAPACITE','ICICIGI','SBILIFE','MAXHEALTH','N100','PIIND','SYMPHONY','RELAXO','ESTER','ASHIANA','DHANUKA','MAITHANALL','BODALCHEM','APLLTD','PANAMAPET','SHAKTIPUMP','TRITURBINE','POLYMED','RUPA','APLAPOLLO','MINDACORP','VSSL','SWANENERGY','KITEX','MAYURUNIQ','ROSSELLIND','ZUARI','CARERATING','INDUSTOWER','REPCOHOME','ORIENTREF','MCX','SCHNEIDER','INDIAMART','OFSS','APTECHT','NUCLEUS','CANBK','VINATIORGA','ADANIPOWER','GLOBUSSPR','OIL','MGL','INEOSSTYRO','ACC','ADANIENT','AEGISCHEM','HAPPSTMNDS','SUDARSCHEM','ISGEC','SUNDRMFAST','SUNPHARMA','MUTHOOTFIN','JUSTDIAL','ATULAUTO','ORIENTCEM','ABFRL','IBULHSGFIN']
# %%
def candle(instrument):
    df=yf.download(instrument+'.NS',period='1d',interval='15m')
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
                    break

                    


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
print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


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
time.sleep(1380)
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
profit=[]
for i in range(len(df)):
    
    if df['type'][i]=='long':
        profit.append(((df['price_out'][i]-df['price_in'][i])/df['price_in'][i])*100)
    elif df['type'][i]=='short':
        profit.append(((df['price_in'][i]-df['price_out'][i])/df['price_out'][i])*100)

df['profit']=np.array(profit)
print(portfolio)

df.to_csv("rachna.csv")


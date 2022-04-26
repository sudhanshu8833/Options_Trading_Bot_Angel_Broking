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
print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

client = FivePaisaClient(email="sudhanshu8833@gmail.com", passwd="Madhya246###", dob="20010626")
client.login()


# %%


tickers=['AARTIIND','ABAN','ALEMBICLcD','AMARAJABAT','SHAREINDIA','ANDHRSUGAR','GODREJAGRO','APCOTEXIND','APOLLOTYRE','ANDHRAPAP','ARVIND','UNIDT','ASHOKLEY','IEX','AAKASH','CHEMCON','AUROPHARMA','GICRE','ANGELBRKG','BALMLAWRIE','BALRAMCHIN','BANARBEADS','NAM-INDIA','BEL','MAHLOG','NIACL','BERGEPAINT','BEPL','BHARATFORG','KHADIM','BHARATGEAR','IFGLEXPOR','BHEL','5PAISA','TATASTLBSL','HDFCLIFE','BIRLACABLE','MAZDOCK','BOMDYEING','BPCL','UTIAMC','RELINFRA','BSL','LIKHITHA','CANFINHOME','GRAPHITE','CARBORUNIV','CENTENKA','CENTURYTEX','CESC','IGARASHI','CHAMBLFERT','EXIDEIND','CHOLAFIN','CIPLA','HEMIPROP','SHALBY','CLNINDIA','TATACOFFEE','COROMANDEL','COSMOFILMS','FSC','DABUR','DALMIASUG','DCM','DCMSHRIRAM','DCW','DEEPAKFERT','DHAMPURSUG','ASTRON','KHAICHEM','EQUITASBNK','EIDPARRY','EIHOTEL','ELGIEQUIP','SUBEXLTD','EPL','EVERESTIND','FACT','FEDERALBNK','FINCABLES','FINPIPE','UFLEX','ZENSARTECH','GABRIEL','GHCL','APOLLO','GICHSGFIN','GIPCL','NEWGEN','GMBREW','GNFC','FMGOETZE','KANSAINER','GREAVESCOT','GSFC','CASTROLIND','GUJALKALI','AMBUJACEM','GFLLIMITED','HARRMALAYA','MARINE','HIMATSEIDE','HINDALCO','HINDOILEXP','HINDPETRO','HSIL','HINDZINC','REPL','IFBAGRO','BURGERKING','SHIVAMILLS','ASTERDM','INDHOTEL','INDIACEM','INDIAGLYCO','INDIANHUME','RKEC','MGEL','INGERRAND','IOC','BECTORFOOD','ITC','HGINFRA','ITI','JAYBARMARU','JAYSREETEA','JINDALPOLY','KANPRPLA','AWHCL','KABRAEXTRU','KAJARIACER','KAKATCEM','KALPATPOWR','KANORICHEM','KARURVYSYA','KCP','KESORAMIND','ACRYSIL','CUMMINSIND','KOPRAN','KSB','TRENT','LIBERTSHOE','LICHSGFIN','AHLADA','M&M','CHENNPETRO','HOMEFIRST','MAHSEAMLES','MANGLMCEM','STOVEKRAFT','BDL','SUNDARMHLD','MOREPENLAB','BANDHANBNK','MRPL','BESTAGRO','MUNJALSHOW','HEIDELBERG','NCC','SMCGLOBAL','NAVNETEDUL','NELCO','SANDHAR','RAILTEL','NOCIL','CENTRUM','MIDHANI','ONGC','ISEC','SILGO','BCLIND','HUHTAMAKI','LEMONTREE','HERANBA','PHILIPCARB','PRAKASH','PRECWIRE','PRSMJOHNSN','JUBLINGREA','EASEMYTRIP','RSWM','RALLIS','ANURAS','LXCHEM','RANEHOLDIN','RAYMOND','RCF','HITECH','RICOAUTO','RIIL','RUBYMILLS','KALYANKJIL','SAIL','SURYODAY','ORIENTELEC','SANGHIIND','WONDERLA','NETFSDL26','JINDALSAW','SBIN','SCI','VEDL','SESHAPAPER','SHANTIGEAR','INDOSTAR','SHREDIGCEM','SHREYANIND','BARBEQUE','SHREYAS','SIMPLEXINF','LODHA','JTEKTINDIA','SPIC','TEMBO','STARPAPER','DEEPINDS','SURYAROSNI','SMLISUZU','AGARIND','TATACHEM','TATAPOWER','TATACONSUM','TATAMOTORS','TFCILTD','THOMASCOOK','TINPLATE','TIRUMALCHM','TNPETRO','UCALFUEL','UNICHEMLAB','UNIVCABLES','JUBLPHARMA','VIPIND','VLSFINANCE','WALCHANNAG','WATERBASE','RITES','WHEELS','WIPRO','WSTCSTPAPR','ZEEL','ZODIACLOTH','ZUARIGLOB','TOKYOPLAST','VARROC','SOMANYCERA','HATSUN','CAPLIPOINT','PREMIERPOL','GOCLCORP','TNPL','GREENPLY','CORALFINAC','NBVENTURES','AUSOMENT','JAYAGROGN','PANACEABIO','MARICO','TCNSBRANDS','MOTHERSUMI','VISAKAIND','DENORA','STERTOOLS','GULFOILLUB','MIRZAINT','JAGSNPHARM','CREDITACC','JMCPROJECT','HITECHGEAR','ELECTHERM','AARTIDRUGS','SIGIND','RAMCOIND','KOTHARIPET','HERITGFOOD','BANKBARODA','GAIL','SKMEGGPROD','BANKINDIA','INDNIPPON','CONCOR','INDRAMEDCO','SNOWMAN','INDSWFTLAB','FDC','ENGINERSIN','ICICIBANK','IRCON','SHARDACROP','CIGNITITEC','JAICORPLTD','GMDCLTD','ASAHIINDIA','TRIGYN','GRSE','KOTHARIPRO','ITDCEM','CUB','CYIENT','KOTAKBKETF','AXISBANK','INTELLECT','MONTECARLO','CYBERTECH','GOODLUCK','FCL','CAMLINFINE','DTIL','GULPOLY','MAN50ETF','NATIONALUM','LAMBODHARA','RSSOFTWARE','TECHNOE','SONATSOFTW','MOLDTKPAC','JINDALSTEL','MENONBE','BSOFT','JMA','HCLTECH','SETFNIFBK','STAR','RAJESHEXPO','GLENMARK','WOCKPHARMA','ZENTEC','TREJHARA','NRBBEARING','RAMCOSYS','INOXWIND','GEPIL','CADILAHC','AVANTIFEED','MAHLIFE','KTKBANK','RPSGVENT','SPENCERS','BLUESTARCO','XELPMOC','TVSMOTOR','NETFMID150','CHALET','NLCINDIA','VETO','VRLLOG','PNBGILTS','GAEL','USHAMART','NOVARTIND','ANUP','UFO','ARVINDFASN','BALAJITELE','STLTECH','TAJGVK','MSTCLTD','PNCINFRA','SKIPPER','AXISCADES','SAKAR','MAHESHWARI','HIKAL','KPITTECH','SMARTLINK','NEOGEN','EMAMIPAP','GODREJCP','SETFNIF50','CONFIPET','SYNGENE','KAYA','AYMSYNTEX','PPL','RAMASTEEL','MAJESCO','STEELCITY','MUTHOOTCAP','MCDOWELL-N','SATIN','ARVSMART','POWERMECH','SHARDAMOTR','NAVKARCORP','NIFTYBEES','KRBL','MARKSANS','TCI','SHREEPUSHK','GUJGASLTD','BHARTIARTL','OLECTRA','PONNIERODE','PNB','OMAXAUTO','GODREJIND','JUNIORBEES','STCINDIA','RADICO','INFOBEAN','ICICIBANKN','DCMNVL','SATIA','SIRCA','SECURKLOUD','NATHBIOGEN','LIBAS','CREATIVE','IDFCFIRSTB','SHK','VARDHACRLC','SUVEN','JSL','WELSPUNIND','JAIBALAJI','IGL','TVSELECT','DREDGECORP','TVTODAY','UPL','UNIENTER','PETRONET','PTC','VAIBHAVGBL','TTKHLTCARE','BIOCON','UMANGDAIRY','ZOTA','SALZERELEC','RKFORGE','DATAMATICS','NDTV','SPANDANA','BANKBEES','SPICEJET','CCL','APARINDS','NIITLTD','TEXINFRA','WESTLIFE','GULFPETRO','LINCOLN','GUFICBIO','ASTRAMICRO','WELENT','NTPC','KOTARISUG','JBMA','DWARKESH','INDOCO','SUPRAJIT','XCHANGING','JSWSTEEL','GDL','VISHAL','GOKEX','EVEREADY','SHOPERSTOP','MANGALAM','WELCORP','NH','JKPAPER','GRANULES','MANINDS','GEOJITFSL','GENUSPOWER','NECLIFE','SPLIL','IDFC','GOLDIAM','RML','ICIL','AURIONPRO','DOLAT','JSLHISAR','SWSOLAR','PRECAM','IIFLSEC','SORILINFRA','TRIVENI','VIMTALABS','NAHARINDUS','QUICKHEAL','NITINSPIN','ROHLTD','ENIL','GSPL','JAGRAN','INOXLEISUR','SADBHAV','KEC','INDOTECH','M&MFIN','CENTURYPLY','KEI','GALLANTT','VAKRANGEE','UTTAMSUGAR','BHAGERIA','SUNTV','RSYSTEMS','EMKAY','KELLTONTEC','KAMDHENU','PIONEEREMB','JKLAKSHMI','ALLCARGO','MUNJALAU','EMAMILTD','VIDHIING','ACE','SELAN','JMFINANCIL','ELECON','TALBROAUTO','GEECEE','GATI','VISHWARAJ','FIEMIND','DCBBANK','INSPIRISYS','GESHIP','TORNTPOWER','SUTLEJTEX','DAAWAT','RUCHIRA','SOBHA','DONEAR','VENUSREM','KUANTUM','JINDRILL','BANCOINDIA','HIRECT','CREST','PLASTIBLEN','NFL','HBLPOWER','JASH','AVTNPL','LUMAXTECH','SANGHVIMOV','IGPL','SIYSIL','PTL','AUTOIND','NETWORK18','GANDHITUBE','PITTIENG','MINDAIND','IZMO','TV18BRDCST','TIIL','REDINGTON','ORIENTBELL','SEQUENT','PFC','FSL','INDIANB','SMSPHARMA','HSCL','GANESHHOUC','LAOPALA','GOLDBEES','JKTYRE','NAHARSPING','NAHARPOLY','IBREALEST','KIRLFER','GOKULAGRO','THEMISMED','NCLIND','BANSWRAS','GOLDSHARE','PHOENIXLTD','AROGRANITE','BFUTILITIE','SRHHYPOLTD','FORTIS','ALPHAGEO','WEBELSOLAR','CHEMBOND','INSECTICID','MCDHOLDING','GUJAPOLLO','GOACARBON','TIMETECHNO','DLF','NELCAST','V2RETAIL','TARMAT','SPARC','ADSL','DECCANCE','OMAXE','ASIANTILES','TAKE','PURVA','SRIPIPES','MAHINDCIE','MOTILALOFS','CSBBANK','KSCL','POWERGRID','MANGCHEFER','MAANALU','DELTACORP','RELIGARE','ADANIPORTS','EDELWEISS','KOLTEPATIL','RGL','JYOTHYLAB','MADHAV','HITECHCORP','BRIGADE','BGRENERGY','MANAKSIA','ARIES','PPAP','DVL','BIRLAMONEY','JKIL','CORDSCABLE','ONMOBILE','KNRCON','HERCULES','IRB','NMDC','RAIN','SHALPAINTS','GSS','RECLTD','NAHARCAP','VGUARD','DHANI','EIHAHOTELS','NESCO','TWL','HCG','PRINCEPIPE','BHARATWIRE','INFIBEAM','PANACHE','MMP','VAISHALI','KIRIINDUS','RPGLIFE','GET&D','VINYLINDIA','KOKUYOCMLN','EQUITAS','DPWIRES','20MICRONS','JOCIL','ALKALI','TATAMTRDVR','MAWANASUG','HINDNATGLS','UJJIVAN','CROMPTON','SUMICHEM','PARAGMILK','ALBERTDAVD','BLS','AJMERA','MHRIL','AMRUTANJAN','ASALCBR','MAHEPC','MOLDTECH','SUNTECK','POKARNA','GPTINFRA','QUESS','DEN','SHILPAMED','SARDAEN','REFEX','DLINKINDIA','JSWENERGY','DBCORP','HINDCOPPER','SUVENPHAR','MMTC','SBICARD','TRF','ADVENZYMES','MINDTECK','DBL','KOTAKNIFTY','THANGAMAYL','EMMBI','TEXMOPIPES','MANINFRA','DEEPENR','SPAL','LGBBROSLTD','FRETAIL','RBLBANK','ASIANHOTNR','ISFT','CUPID','GNA','ICICIPRULI','MARATHON','HPL','VERTOZ','KSL','PNBHOUSING','VBL','PIONDIST','MANAPPURAM','AARVI','KIOCL','CMICABLES','HMVL','LAURUSLABS','IMFA','BLISSGVS','DFMFOODS','EMAMIREAL','TERASOFT','ITDC','HISARMETAL','BOROLTD','BAJAJCON','HDFCMFGETF','BSE','PRICOLLTD','ICICIGOLD','GPPL','SASTASUNDR','INTENTECH','CAREERP','RAMKY','GALLISPAT','CANTABIL','AKSHARCHEM','ASHOKA','WABAG','CLEDUCATE','OBEROIRLTY','PRESTIGE','NRAIL','SHANKARA','RESPONIND','CGCL','COALINDIA','IOLCP','NACLIND','APCL','AXISGOLD','GRAVITA','DOLLAR','SUPERHOUSE','JINDWORLD','SCHAND','RPPINFRA','BHAGYANGR','JAMNAAUTO','HUDCO','MOIL','PSPPROJECT','KIRLOSENG','STARCEMENT','BFINVEST','ERIS','CDSL','GTPL','ICICILOVOL','DYNPRO','STEELXIND','SALASAR','MAGADSUGAR','AVADHSUGAR','STEL','SIS','COCHINSHIP','JUBLINDS','SMSLIFE','ABCAPITAL','APEX','DCAL','LASA','CHOLAHLDNG','CAPACITE','DIAMONDYD','HFCL','INDTERRAIN','WORTH','MACPOWER','ICICITECH','MAXHEALTH','TOTAL','MAXIND','N100','ESTER','ASHIANA','DHANUKA','FILATEX','L&TFH','BODALCHEM','BROOKS','TDPOWERSYS','APLLTD','PGEL','PANAMAPET','PAISALO','SHAKTIPUMP','TRITURBINE','DSSL','POLYMED','RUPA','MINDACORP','TBZ','VSSL','SWANENERGY','SPECIALITY','CINELINE','KITEX','MAYURUNIQ','ROSSELLIND','ZUARI','CARERATING','INDUSTOWER','ICICINIFTY','REPCOHOME','GSCLCEMENT','ORIENTREF','SCHNEIDER','NBCC','APTECHT','NUCLEUS','CANBK','SEYAIND','ADANIPOWER','GLOBUSSPR','OIL','MAXVIL','CONTROLPR','EXPLEOSOL','MAHASTEEL','ADORWELD','AEGISCHEM','HAPPSTMNDS','MODISNME','SUBROS','SUDARSCHEM','ISGEC','SUNDRMFAST','SUNFLAG','SUNPHARMA','JUSTDIAL','CEREBRAINT','ATULAUTO','ORIENTCEM','ABFRL','IBULHSGFIN','FLFL']
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
kickers=[]


# ohlcv_database=pd.DataFrame()
# price_in=[]
# price_out=[]
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
    
    global ltp,price,tickers,prise,position,kickers
    
    # ohlc_dict=pd.DataFrame()
    # ohlc_dict=candle(int(instrument))    
    # prise=ohlc_dict["Close"].iloc[-1]


    signal=""
    if l_s=="":
    
        if ((prise[instrument]-ltp[instrument])/prise[instrument])*100>2 and  ((prise[instrument]-ltp[instrument])/prise[instrument])*100<8:
            signal="buy"
            kickers.append(instrument)

        elif ((prise[instrument]-ltp[instrument])/prise[instrument])*100<-2 and  ((prise[instrument]-ltp[instrument])/prise[instrument])*100>-8:
            signal="sell"
            kickers.append(instrument)

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
    
    for i in range(17):

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
            # print(ticker)
            # print(ltp[ticker])
            # # print"(****************)"
            # print(prise[ticker])
            j+=1



        
        # for ticker in tickers[50*i:50*i+49]:

        #     if ltp[ticker]==0:
        #         tickers.remove(ticker)
        #         ltp.pop(ticker,None)
        #         prise.pop(ticker,None)
        #         print("dvgbhnjmxdcfgvhbnjdcvghbjnmdcgvhb jnmdctvgbhnjdcvgbh")
                
        #     if prise==0:
        #         tickers.remove(ticker)
        #         prise.pop(ticker,None)
        #         ltp.pop(ticker,None)
        #         print("dvgbhnjmxdcfgvhbnjdcvghbjnmdcgvhb jnmdctvgbhnjdcvgbh")
                
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
            
            # else:
            #     position[ticker='none']
    # except:
    #         print("something went wrong... moving to next iteration")
    # print("###############################")   





# %%
# time.sleep(57)
start_time=time.time()
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

timeout=start_time+4
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

print(kickers)


def market_order2(instrument,investment,risk):
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
def market_order12(instrument,investment):
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

def trade_signal1(instrument,l_s):
    
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
            kickers.remove(instrument)
                        
      

    elif l_s=="long":
        if ltp>= 0.80*(abs(prise-price[instrument]))+price[instrument] or ltp<=price[instrument]-0.80*(abs(prise-price[instrument])):

            signal="squareoffsell"
            kickers.remove(instrument)

           
                    
    elif l_s=="short":
        if ltp>= (0.80*(abs(prise-price[instrument]))+price[instrument]) or ltp<=(price[instrument]-0.80*(abs(prise-price[instrument]))):
            signal="squareoffbuy"
            kickers.remove(instrument)
            


    return signal    





def main1():
    global kickers,investment,risk,ltp,position,prise
    
    for ticker in kickers.copy():
        # try:
        req_list_=[{"Exch":"N","ExchType":"C","Symbol":ticker}]
            
        data=client.fetch_market_feed(req_list_)
        ltp=float(data['Data'][0]['LastRate'])
        prise=float(data['Data'][0]['PClose'])        
        if ltp==0:
            kickers.remove(ticker)
            continue
        if prise==0:
            kickers.remove(ticker)
            continue
        print("\n \n analyzzing for ",ticker)
        print(ltp)


        l_s= position[ticker]
        print(l_s)
        signal=trade_signal1(ticker,l_s)
        if signal=="buy":
            market_order2(ticker,investment,risk)
            print("New long position initiated for ",ticker)

        elif signal=="sell":
            market_order2(ticker,-1*investment,risk)
            print("New short position initiated for ", ticker)

        elif signal=="squareoffbuy":
            market_order12(ticker,investment)

        elif signal=="squareoffsell":
            market_order12(ticker,-1*investment)
        # except:
        #     print("something went wrong... moving to next iteration")



start_time=time.time()
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
timeout=start_time+300
while time.time()<=timeout:
    try:
    #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@") 
    #     print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@") 
        print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        main1()
        # print("porfolio: ",portfolio)

        # time.sleep(300-(time.time()-start_time)%300)
        
    except KeyboardInterrupt:
        print("keyboard interuption ....... exiting")

for ticker in kickers.copy():
    # req_list_=[{"Exch":"N","ExchType":"C","Symbol":ticker}]
        
    # data=client.fetch_market_feed(req_list_)
    # ltp=float(data['Data'][0]['LastRate'])        
    # if ltp==0:
    #     tickers.pop(ticker,None)
    #     continue
    # print("\n \n analyzzing for ",ticker)
    # print(ltp)
    if position[ticker]=="long":
        market_order12(ticker,-1*investment)

    if position[ticker]=="short":
        market_order12(ticker,investment)     



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








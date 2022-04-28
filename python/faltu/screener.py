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

tickers=["AARTIIND","ABFRL","ACC","ADANIENT","ADANIPORTS","ALKEM","AMARAJABAT","AMBUJACEM","APLLTD","APOLLOHOSP","APOLLOTYRE","ASHOKLEY","ASIANPAINT","AUBANK","AUROPHARMA","AXISBANK","BAJAJ-AUTO","BAJAJFINSV","BAJFINANCE","BALKRISIND","BANDHANBNK","BANKBARODA","BATAINDIA","BEL","BERGEPAINT","BHARATFORG","BHARTIARTL","BHEL","BIOCON","BOSCHLTD","BPCL","BRITANNIA","CADILAHC","CANBK","CHOLAFIN","CIPLA","COALINDIA","COFORGE","COLPAL","CONCOR","COROMANDEL","CUB","CUMMINSIND","DABUR","DEEPAKNTR","DIVISLAB","DLF","DRREDDY","EICHERMOT","ESCORTS","EXIDEIND","FEDERALBNK","GAIL","GLENMARK","GMRINFRA","GODREJCP","GODREJPROP","GRANULES","GRASIM","GUJGASLTD","HAVELLS","HCLTECH","HDFC","HDFCAMC","HDFCBANK","HDFCLIFE","HEROMOTOCO","HINDALCO","HINDPETRO","HINDUNILVR","IBULHSGFIN","ICICIBANK","ICICIGI","ICICIPRULI","IDEA","IDFCFIRSTB","IGL","INDHOTEL","INDIGO","INDUSINDBK","INDUSTOWER","INFY","IOC","IRCTC","ITC","JINDALSTEL","JSWSTEEL","JUBLFOOD","KOTAKBANK","L&TFH","LALPATHLAB","LICHSGFIN","LT","LTI","LTTS","LUPIN","M&M","M&MFIN","MANAPPURAM","MARICO","MARUTI","MCDOWELL-N","METROPOLIS","MFSL","MGL","MINDTREE","MOTHERSUMI","MPHASIS","MRF","MUTHOOTFIN","NAM-INDIA","NATIONALUM","NAUKRI","NAVINFLUOR","NESTLEIND","NMDC","NTPC","ONGC","PAGEIND","PEL","PETRONET","PFC","PFIZER","PIDILITIND","PIIND","PNB","POWERGRID","PVR","RAMCOCEM","RBLBANK","RECLTD","RELIANCE","SAIL","SBILIFE","SBIN","SHREECEM","SIEMENS","SRF","SRTRANSFIN","SUNPHARMA","SUNTV","TATACHEM","TATACONSUM","TATAMOTORS","TATAPOWER","TATASTEEL","TCS","TECHM","TITAN","TORNTPHARM","TORNTPOWER","TRENT","TVSMOTOR","UBL","ULTRACEMCO","UPL","VEDL","VOLTAS","WIPRO","ZEEL"]
							


def candle(instrument):
    df=client.historical_data('N','C',instrument,'1d','2021-06-20','2021-06-26')
    return df


df=pd.read_csv(r'scripmaster-csv-format.csv')

scripcode=[]
symbol=[]

for i in range(len(df)):
    if df['Exch'][i]=='N' and df["ExchType"][i]=='C' and df["Series"][i] == 'EQ':
        scripcode.append(df['Scripcode'][i])
        symbol.append(df['Name'][i])

ohlc_dict=pd.DataFrame()
ohlc_dict['scripcode']=np.array(scripcode)
ohlc_dict['symbol']=np.array(symbol)
ohlc_opg=pd.DataFrame()
symbol1=[]
scripcode1=[]
stocks=[]
k=1
for i in range(len(ohlc_dict)):
    try:
        print("sahi hai",i)
        df=candle(int(ohlc_dict['scripcode'][i]))
        if df['Volume'].iloc[-1]<500000 and df['Volume'].iloc[-1]>100000 and df['Close'].iloc[-1]>100 and df['Close'].iloc[-1]<1000:
            symbol1.append(ohlc_dict['symbol'][i])
            # scripcode1.append(ohlc_dict['scripcode'][i])
    except:
        print("moving aage: ",k)
        # k+=1
        # stocks.append(ohlc_dict['symbol'])
# ohlc_opg['scripcode1']=np.array(scripcode1)
# ohlc_opg['symbol1']=np.array(symbol1)

print(symbol1)
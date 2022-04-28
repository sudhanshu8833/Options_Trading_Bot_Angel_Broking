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






df=pd.read_csv(r'scrip code angelbroking.csv')

scripcode=[]
symbol=[]





# %%
token=[]
symbol=[]

    
for i in range(len(df)):
    if df['exch_seg'][i]=='NSE' and '-EQ' in df['symbol'][i]:
        
        symbol.append(df['symbol'][i])
        scripcode.append(df['token'][i])
        


# %%
for i in range(len(symbol)):
    symbol[i]=symbol[i].replace("-EQ",".NS")
ohlc_dict=pd.DataFrame()
ohlc_dict['scripcode']=np.array(scripcode)
ohlc_dict['symbol']=np.array(symbol)
ohlc_opg=pd.DataFrame()
symbol1=[]
scripcode1=[]
stocks=[]


# %%

for i in range(len(ohlc_dict)):
    try:
    
        print("sahi hai",i)
        data=yf.Ticker(str(ohlc_dict['symbol'][i])).info
        if data['currentPrice']>20 and data['marketCap']>3000000000:
            symbol1.append(ohlc_dict['symbol'][i])
            scripcode1.append(ohlc_dict['scripcode'][i])
    except:
        print("thoda problem hai ")

print(symbol1)
df1=pd.DataFrame()
df1['scripcode']=np.array(scripcode1)
df1['symbol']=np.array(symbol1)
df1.to_csv("df.csv")


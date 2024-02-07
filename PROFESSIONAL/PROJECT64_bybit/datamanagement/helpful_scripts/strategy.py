import pandas as pd
import time
import traceback
from datetime import datetime
import logging
import json
import certifi
from finta import TA
import ccxt

from datamanagement.models import *
from datamanagement.helpful_scripts.background_functions import *



#CONFIGURATIONS
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger('dev_log')
error = logging.getLogger('error_log')

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
data={}
with open("background.json") as json_file:
    data=json.load(json_file)

client = MongoClient(data['mongo_uri'], server_api=ServerApi('1'),connect=False,tlsCAFile=certifi.where())
database=client[data['database']]
admin=database['admin']
position=database['position']
current_candles=database['candles']

'''
# ADMIN
{   "username":"",
    "password":"",
    "api_key":"",
    "secret_key":"",
    "investment":,
    "symbols":["BTC/USDT","ETH/USDT"],
    "status":True | False,
    "live": True | False,
    "EMA_1_period":"",
    "EMA_2_period":"",
    "time_frame":"5m"
    "stoploss":"",
    "takeprofit":""
}

# POSITION
{
    "symbol":"",
    "status": OPEN | CLOSED,
    "type": LONG | SHORT,
    "time_start":"",
    "time_end":"",
    "quantity":"",
    "pnl":"",
    "current_price":"",
    "price_in":"",
    "price_out":"",
    "stoploss":"",
    "take_profit":""
}
'''

class run_strategy():
    count=0

    def __init__(self):
        self.ltp_prices={}
        self.times=time.time()
        
        self.admin=admin.find_one()
        self.login()
        self.prices={}
        run_strategy.count+=1

    def login(self):
        self.client=ccxt.bybit({
            'apiKey':self.admin['api_key'],
            "secret":self.admin['secret_key'],
            'enableRateLimit': True
        })


    def update_candles(self,df):
        data_structure = [
            {
                "time": index,
                "open": row['open'],
                "high": row['high'],
                "low": row['low'],
                "close": row['close'],
                "volume": row['volume'],
                "EMA1": row['EMA1'],
                "EMA2": row['EMA2']
            }
            for index, row in df.iterrows()
        ]
        data_structure={"data":data_structure}
        current_candles.update_one({},{"$set":data_structure})

    def download_ohlc(self,instrument):
        data=self.client.fetch_ohlcv(instrument,timeframe=self.admin['time_frame'])
        df=pd.DataFrame(data,columns=['Datetime','open','high','low','close','volume'])
        df.index=df['Datetime']
        df.drop(columns=['Datetime'],inplace=True)
        df = df.apply(pd.to_numeric)
        df['EMA1']=TA.EMA(df,self.admin['EMA_1_period'])
        df['EMA2']=TA.EMA(df,self.admin['EMA_2_period'])
        self.prices[instrument]=df['close'].iloc[-1]
        self.update_candles(df)
        return df[:-1]


    def add_positions(self,instrument,type):
        price=self.prices[instrument]

        takeprofit,stoploss=[0,0]
        if(type=="buy"):
            takeprofit=price*(1+(self.admin['takeprofit'])/100.0)
            stoploss=price*(1-(self.admin['stoploss'])/100.0)
            type="LONG"

        elif(type=="sell"):
            takeprofit=price*(1-(self.admin['takeprofit'])/100.0)
            stoploss=price*(1+(self.admin['stoploss'])/100.0)
            type="SHORT"

        pos={
            "symbol":instrument,
            "status":"OPEN",
            "type":type,
            "time_start":datetime.now(),
            "time_end":datetime.now(),
            "quantity":float(self.admin['investment']/self.prices[instrument]),
            "current_price":self.prices[instrument],
            "price_in":self.prices[instrument],
            "price_out":0,
            "stoploss":stoploss,
            "take_profit":takeprofit,
            "pnl":0
        }
        position.insert_one(pos)

        if(self.admin['live']):
            self.create_order(pos)

    def is_position(self,instrument):
        positions=list(position.find())

        for pos in positions:
            if(instrument==pos['symbol'] and pos['status']=='OPEN'):
                return True

        return False


    def create_order(self,params):

        try:
            if(params['status']=="OPEN"):
                if(params['type']=='LONG'):
                    self.client.create_order(params['symbol'],'market','buy',params['quantity'],self.prices[params['symbol']])
                else:
                    self.client.create_market_sell_order(params['symbol'],self.admin['investment'])

            if(params['status']=="CLOSED"):
                if(params['type']=='SHORT'):
                    self.client.create_order(params['symbol'],'market','buy',params['quantity'],self.prices[params['symbol']])

                else:
                    base=params['symbol'].split('/')[0]
                    self.client.create_market_sell_order(params['symbol'],self.balance[base])

        except Exception:
            error.info(str(traceback.format_exc()))



    def signals(self,instrument,df):
        if(not self.is_position(instrument)):
            if(df['EMA1'].iloc[-1]<df['EMA2'].iloc[-1] and df['EMA1'].iloc[-2]>df['EMA2'].iloc[-2]):
                return 'buy'

            elif(df['EMA1'].iloc[-1]>df['EMA2'].iloc[-1] and df['EMA1'].iloc[-2]<df['EMA2'].iloc[-2]):
                return 'sell'

        return "NA"
    
    
    def close_signal(self):
        positions=position.find()

        for pos in positions:
            if(pos['status']=="OPEN"):
                pos['current_price']=self.prices[pos['symbol']]
                if(pos['type']=='LONG'):
                    pos['pnl']=round(pos['current_price']-pos['price_in'],2)
                    if(pos['current_price']>=pos['take_profit'] or pos['current_price']<=pos['stoploss']):

                        pos['status']='CLOSED'
                        pos['time_end']=datetime.now()
                        pos['price_out']=pos['current_prices']
                        if (self.admin['live']):
                            self.create_order(pos)

                elif(pos['type']=='SHORT'):
                    pos['pnl']=round(pos['price_in']-pos['current_price'],2)
                    if(pos['current_price']<=pos['take_profit'] or pos['current_price']>=pos['stoploss']):

                        pos['status']="CLOSED"
                        pos['time_end']=datetime.now()
                        pos['price_out']=pos['current_prices']
                        
                        if (self.admin['live']):
                            self.create_order(pos)

                position.update_one({"_id":pos['_id']},{"$set":pos})




    def main(self):

        for ticker in self.admin['symbols']:
            df=self.download_ohlc(ticker)

            signal=self.signals(ticker,df)

            if(signal=="buy"):
                self.add_positions(ticker,signal)

            elif(signal=="sell"):
                self.add_positions(ticker,signal)



        self.close_signal()


    def run(self):
        try:
            while True:
                if(self.admin['status']):

                    self.admin=admin.find_one()
                    self.balance=self.client.fetch_free_balance()
                    self.main()
                else:
                    time.sleep(60)

        except Exception:
            error.info(str(traceback.format_exc()))
            return str(traceback.format_exc())

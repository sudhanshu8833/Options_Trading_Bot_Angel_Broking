import numpy as np
import pandas as pd
import datetime
import time
#from decimal import Decimal
import pandas as pd
from pandas.tseries.offsets import BDay
import requests
from datetime import date,timedelta
#import simplejson as json
import json
import os
import pytz

from account import API_KEY, ACCOUNT_ID, REFRESH_TOKEN
from account import get_access_token



BASE = 'https://api.tdameritrade.com/v1/'
ACCOUNTS = BASE + 'accounts/'
SEARCH = BASE + 'instruments'
INSTRUMENTS = SEARCH + '/'
QUOTE = BASE + 'marketdata/%s/quotes'
HISTORY = BASE + 'marketdata/%s/pricehistory'
OPTION_CHAINS = BASE + 'marketdata/chains'
QUOTES='https://api.tdameritrade.com/v1/marketdata/quotes'


def get_price_history(symbol='AAPL', periodType='day', period='2', frequencyType='minute', frequency='1', needExtendedHoursData='false', access_token = None):
    if access_token is None:
        return
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json',
        }
    params = (
        #('apikey', 'DEARSOURABH99'),
        ('periodType', periodType),
        ('period', period),
        ('frequencyType', frequencyType),
        ('frequency', frequency),
        ('needExtendedHoursData', needExtendedHoursData),
        )
    res = requests.get(HISTORY % symbol, headers=headers, params=params).json()
    if res['empty'] is True: 
        return None
    df = pd.DataFrame(res['candles'])
    
    
    
    
    fcn = lambda x: datetime.datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d %H:%M:%S')
    df['datetime'] = pd.to_datetime(df['datetime'].map(fcn))
    
    
    
    UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
    fcn2 = lambda x: (x + UTC_OFFSET_TIMEDELTA).tz_localize('UTC').tz_convert('US/Eastern').replace(tzinfo=None)
    df['datetime'] = pd.to_datetime(df['datetime'].map(fcn2))
    
    
    return df#.set_index('datetime')


def get_price_history_between_times(symbol='AAPL', periodType='day', period='2', frequencyType='minute', frequency='1',
                                    needExtendedHoursData='false', access_token = None):
    if access_token is None:
        return
    
    #time.sleep(1)
    
    now_ = datetime.datetime.now()
    tz = pytz.timezone('US/Eastern')
    now = now_.astimezone(tz)
    
    #print(now)
    #now = now - pd.Timedelta(minutes=1)
    #print(now)
    
    #start = now - BDay(int(period))
    #startTimeEpoch = int(1000*datetime.datetime(start.year, start.month, start.day, start.hour, start.minute).timestamp())
    
    
    #print(type(startTimeEpoch))
    
    #endTimeEpoch = int(1000*datetime.datetime(now.year, now.month, now.day, now.hour, now.minute).timestamp())
    
    
    tm = time.time()
    endTimeEpoch = int(tm*1000)
    startTimeEpoch = int(endTimeEpoch - int(period)*24*60*60*1000)
    
    #print(startTimeEpoch)
    #print(endTimeEpoch)
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json',
        }
    params = (
        #('apikey', 'DEARSOURABH99'),
        #('periodType', periodType),
        #('period', period),
        ('frequencyType', frequencyType),
        ('frequency', frequency),
        ('startDate', startTimeEpoch),
        ('endDate', endTimeEpoch),
        ('needExtendedHoursData', needExtendedHoursData),
        )
    res = requests.get(HISTORY % symbol, headers=headers, params=params).json()
    if res['empty'] is True: 
        return None
    
    #print(len(res['candles']))
    
    df = pd.DataFrame(res['candles'])
    
    #print(len(df))
    df = df.drop_duplicates(subset=['datetime'])
    #print(len(df))
    
    
    fcn = lambda x: datetime.datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d %H:%M:%S')
    df['datetime'] = pd.to_datetime(df['datetime'].map(fcn))
    
    #print(len(df))
    
    
    UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
    fcn2 = lambda x: (x + UTC_OFFSET_TIMEDELTA).tz_localize('UTC').tz_convert('US/Eastern').replace(tzinfo=None)
    df['datetime'] = pd.to_datetime(df['datetime'].map(fcn2))
    
    #print(len(df))
    #df.to_csv('fetched.csv')
    
    #print(df['datetime'].head())
    #print(df['datetime'].tail())
    return df#.set_index('datetime')



def get_price_history_recent(symbol='AAPL', intervals=60, frequencyType='minute', frequency='1',
                                    needExtendedHoursData='false', access_token = None):
    if access_token is None:
        return
    
    #time.sleep(1)
    
    now_ = datetime.datetime.now()
    tz = pytz.timezone('US/Eastern')
    now=now_.astimezone(tz)
    
    #print(now)
    #now = now - pd.Timedelta(minutes=1)
    #print(now)
    
    #start = now - pd.Timedelta(minutes=period)
    #startTimeEpoch = int(1000*datetime.datetime(start.year, start.month, start.day, start.hour, start.minute).timestamp())
    
    
    #print(type(startTimeEpoch))
    
    #endTimeEpoch = int(1000*datetime.datetime(now.year, now.month, now.day, now.hour, now.minute).timestamp())
    
    tm = time.time()
    endTimeEpoch = int(tm*1000)
    startTimeEpoch = int(endTimeEpoch - intervals*60*1000)
    
    
    #print(startTimeEpoch)
    #print(endTimeEpoch)
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json',
        }
    params = (
        #('apikey', 'DEARSOURABH99'),
        #('periodType', periodType),
        #('period', period),
        ('frequencyType', frequencyType),
        ('frequency', frequency),
        ('startDate', startTimeEpoch),
        ('endDate', endTimeEpoch),
        ('needExtendedHoursData', needExtendedHoursData),
        )
    
    #print("making recent request:")
    
    res = requests.get(HISTORY % symbol, headers=headers, params=params).json()
    
    #print("res recent:",res)
    
    if res['empty'] is True: 
        return None
    
    df = pd.DataFrame(res['candles'])
    fcn = lambda x: datetime.datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d %H:%M:%S')
    df['datetime'] = pd.to_datetime(df['datetime'].map(fcn))
    
    
    
    UTC_OFFSET_TIMEDELTA = datetime.datetime.utcnow() - datetime.datetime.now()
    fcn2 = lambda x: (x + UTC_OFFSET_TIMEDELTA).tz_localize('UTC').tz_convert('US/Eastern').replace(tzinfo=None)
    df['datetime'] = pd.to_datetime(df['datetime'].map(fcn2))
    
    
    #print(df.loc[0,'datetime'])
    #print(df.loc[len(df)-1,'datetime'])
    return df#.set_index('datetime')


'''
def get_positions(access_token = None):
    if access_token is None:
        return
    positions = None
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json',
        }
    
    params = (
    ('fields', 'positions'),
    )

    response = requests.get(ACCOUNTS+ACCOUNT_ID, headers=headers, params=params).json()
    
    try:
        positions = response["securitiesAccount"]["positions"]
    except:
        positions = None
    
    return positions
'''


def get_positions():
    try:
        ACCESS_TOKEN = get_access_token()    
    except:
        print('access token fetch failed')
        return None
    
    position_list = []
    
    headers = {
            'Authorization': 'Bearer ' + ACCESS_TOKEN,
            'Content-Type': 'application/json',
        }
    
    params = (
    ('fields', 'positions'),
    )

    response = requests.get(ACCOUNTS+ACCOUNT_ID, headers=headers, params=params).json()
    
    print(response)
    try:
        positionResponse = response["securitiesAccount"]['positions']
        for e in positionResponse:
            symbol = e['instrument']['symbol']
            position = {}
            position[symbol]= symbol
            position['shortQuantity'] = e["shortQuantity"]
            position['longQuantity'] = e["longQuantity"]
            position['currentDayProfitLoss'] = e["currentDayProfitLoss"]
            position_list.append(position)
                
    except:
        print('get position error')
        #positions = None
    
    return position_list





def get_symbol_positions(symbol):
    try:
        ACCESS_TOKEN = get_access_token()    
    except:
        print('access token fetch failed')
        return None
    
    #position_list = []
    position = None
    
    headers = {
            'Authorization': 'Bearer ' + ACCESS_TOKEN,
            'Content-Type': 'application/json',
        }
    
    params = (
    ('fields', 'positions'),
    )

    response = requests.get(ACCOUNTS+ACCOUNT_ID, headers=headers, params=params).json()
    
    #print(response)
    try:
        positionResponse = response["securitiesAccount"]['positions']
        for e in positionResponse:
            if symbol == e['instrument']['symbol']:
                position = {}
                position[symbol]= symbol
                position['shortQuantity'] = e["shortQuantity"]
                position['longQuantity'] = e["longQuantity"]
                position['currentDayProfitLoss'] = e["currentDayProfitLoss"]
                break
    except:
        #print('get position error')
        pass
        #positions = None
    
    return position






def get_orders(access_token = None, symbol=None):
    if symbol is None:  return
    if access_token is None:  return
    
    orders = dict()
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json',
        }
    
    params = (
    ('fields', 'orders'),
    )

    response = requests.get(ACCOUNTS+ACCOUNT_ID, headers=headers, params=params).json()
    
    #print(response)
    try:
        ordersResponse = response["securitiesAccount"]['orderStrategies']
        for e in ordersResponse:
            sym = e['orderLegCollection'][0]['instrument']['symbol']
            print(sym, symbol)
            if sym == symbol:
                orders[symbol]= sym
                orders['quantity'] = e['orderLegCollection'][0]["quantity"]
                orders['status'] = e["status"]
    except:
        orders = None
    
    return orders



def place_order(access_token=None, symbol=None, quantity=None, instruction=None, assetType=None, orderType=None, price=None):
    ORDERS = ACCOUNTS + ACCOUNT_ID +'/orders'
        
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json',
    }        

    data1 = {
        "complexOrderStrategyType": "NONE",
        "orderType": orderType,
        "session": "NORMAL",
        "duration": "DAY",
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
        {    
        "instruction": instruction,
        "quantity": quantity,
        "instrument": {
        "symbol": symbol,
         "assetType":assetType
            }
        }
        ]
        }
    
    '''
    data2 = {"complexOrderStrategyType": "NONE","orderType": orderType,"session": "NORMAL","duration": 
    "DAY","orderStrategyType": "SINGLE",
        "orderLegCollection": [{"instruction": instruction,"quantity": quantity,
        "instrument": {"symbol": symbol,"assetType":assetType}}]}
    '''
    '''
    data2 = (
        ("complexOrderStrategyType", "NONE"),
        ("orderType", "MARKET"),
        ("session", "NORMAL"),
        ("duration", "DAY"),
        ("orderStrategyType", "SINGLE"),
        ("orderLegCollection",
            (    
              ("instruction", instruction),
               ("quantity", str(quantity)),
                ("instrument", (
                                ("symbol", symbol),
                                ("assetType", assetType)
                               )
                )
            )
        )
    )    
    '''
    
    data = json.dumps(data1)
    rec = requests.post(ORDERS, headers=headers, data=data)
    #print(response.text)
    if rec.status_code == 201:
        res = symbol + '  Order Success!' + rec.text
        print(res)            
    else:
        res = symbol + '  Order Failed?' + rec.text
        print(res)
    return rec
    

    
    
    
    
def place_marketstop_order(access_token=None, symbol=None, quantity=None, instruction=None, child_instruction=None, stop_price=None):
    ORDERS = ACCOUNTS + ACCOUNT_ID +'/orders'
        
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json',
        }        
                      
    data1 = {
        
                "complexOrderStrategyType": "NONE",
                "orderType": "MARKET",
                "session": "NORMAL",
                "duration": "DAY",
                "orderStrategyType": "TRIGGER",
                "orderLegCollection": [
                    {    
                        "instruction": instruction,
                        "quantity": quantity,
                        "instrument": {
                            "symbol": symbol,
                            "assetType": "EQUITY"
                        }
                    }
                ],                
                
                "childOrderStrategies": [
                    {
                      "orderType": "LIMIT",
                      "session": "NORMAL",
                      "price": stop_price,
                      "duration": "DAY",
                      "orderStrategyType": "SINGLE",
                      "orderLegCollection": [
                            {
                          "instruction": child_instruction,
                          "quantity": quantity,
                          "instrument": {
                            "symbol": symbol,
                            "assetType": "EQUITY"
                          }
                        }
                      ]
                    }
                  ]
        
            }
        
    response = requests.post(ORDERS, headers=headers, data=json.dumps(data1))
    #print(response.text)
    return response    
    
    
    
    
'''
def get_orders_by_query(self, accountId, maxResults, status, date):
        body = BASE + 'orders'
        headers = {
            'Authorization': 'Bearer ' + self._token,
        }
        params1 = (
            ('accountId', accountId),
            ('maxResults', maxResults),
            ('status', status),
            ) 
        params2 = (
            ('accountId', accountId),
            ('maxResults', maxResults),
            ('fromEnteredTime', date),
            ('toEnteredTime', date),
            #('fromEnteredTime', '2018-09-08T12:01:07+0000'),
            #('toEnteredTime', '2018-09-08T14:01:07+0000'),
            ) 
        params = params2 if status == "ALL" else params1
        response = requests.get(body, headers=headers, params=params).json()
        return response
'''

def get_quote(symbol, access_token):
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json',
        }
    params = (
    ('apikey', API_KEY),
    )
    return requests.get(QUOTE % symbol,  headers=headers, params=params).json()



def get_quotes(access_token, symbol_list):
    symbols_str = ','.join(symbol_list)
    
    headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json',
    }

    params = (
    ('symbol', symbols_str),#'AAPL,TSLA'
    )
    
    response = requests.get(QUOTES, headers=headers, params=params)
    return response.json()


def option_chain(access_token, symbol, contractType, strikeCount=2, includeQuotes='TRUE', expMonth='OCT'):
    params = (
    #('apikey', 'DEARSOURABH99@AMER.OAUTHAP'),
    ('symbol', symbol),
    ('contractType', contractType),
    ('strikeCount', strikeCount),
    ('includeQuotes', includeQuotes),
    ('expMonth', expMonth),
    #('fromDate', fromDate),
    #('toDate', toDate),
    )
    #headers = {'Authorization': '',}
    headers = {'Authorization': 'Bearer ' + access_token}
    return requests.get(OPTION_CHAINS,
                        headers=headers,
                        params=params).json()



def GetATMOption(access_token, symbol, contractType, strikeCount=2, includeQuotes='TRUE', expMonth='OCT'):
    now_ = datetime.datetime.now()
    tz = pytz.timezone('US/Eastern')
    now = now_.astimezone(tz)
    start = now+BDay(1)
    fromDate = start.strftime("%Y-%m-%d")
    
    then = now+BDay(10)
    toDate = then.strftime("%Y-%m-%d")
    
    print(fromDate, toDate)
    
    params = (
    #('apikey', 'DEARSOURABH99@AMER.OAUTHAP'),
    ('symbol', symbol),
    ('contractType', contractType),
    ('strikeCount', strikeCount),
    ('includeQuotes', includeQuotes),
    #('expMonth', expMonth),
    ('fromDate', fromDate),
    ('toDate', toDate),
    )
    #headers = {'Authorization': '',}
    headers = {'Authorization': 'Bearer ' + access_token}
    optChain = requests.get(OPTION_CHAINS,
                        headers=headers,
                        params=params).json()

    if contractType=='CALL':
        s = optChain["callExpDateMap"]
    else:
        s = optChain["putExpDateMap"]
    s1 = None
    symbolCount = 0
    for key in s:
        s1 = s[key]
        #if contractType=='CALL':
        break
    symbolData = pd.DataFrame(index=list(s1.keys()),columns=['ask','bid','optionSymbol'])
    for key in s1:
        symbolData.loc[key,'ask'] = s1[key][symbolCount]['ask']
        symbolData.loc[key,'bid'] = s1[key][symbolCount]['bid']
        symbolData.loc[key,'optionSymbol'] = s1[key][symbolCount]['symbol']
    
    return symbolData.iloc[0].to_dict()    
        

    
def get_account_detail():
    try:
        ACCESS_TOKEN = get_access_token()    
    except:
        print('access token fetch failed')
        return None
    #if self.accountIds:
    #    for acc in self.accountIds:
    #        resp = requests.get(ACCOUNTS + str(ACCOUNT_ID), headers=self._headers())
    #        if resp.status_code == 200:
    #            ret[acc] = resp.json()
    #        else:
    #            raise Exception(resp.text)
    #else:
    resp = requests.get(ACCOUNTS, headers={'Authorization': 'Bearer ' + ACCESS_TOKEN})
    if resp.status_code == 200:
        print('account access success!')
        #print(resp)
        #for account in resp.json():
        #    ret[account['securitiesAccount']['accountId']] = account
    else:
        raise Exception(resp.text)
    return resp.json()   
        

    
    
    
    
    
    
    
    
    
class TDAmeritrader(object):
    def __init__(self, access_token=None, accountIds=None):
        self._token = access_token or os.environ['ACCESS_TOKEN']
        self.accountIds = accountIds or []
        self.cancelled_flag = pd.Series()
        self.BuyOrderIDData = None
        self.BuyOrderStatusData = None
        self.FilledBuyOrderIDData = None
        self.CancelledBuyOrderIDData = None
        self.SellOrderIDData = None
        self.SellOrderStatusData = None
        self.FilledSellOrderIDData = None
        self.CancelledSellOrderIDData = None
        self.FilledBuyOrderData = None        
    def _headers(self):
        return {'Authorization': 'Bearer ' + self._token}
    def accounts(self):
        ret = {}
        if self.accountIds:
            for acc in self.accountIds:
                resp = requests.get(ACCOUNTS + str(acc), headers=self._headers())
                if resp.status_code == 200:
                    ret[acc] = resp.json()
                else:
                    raise Exception(resp.text)
        else:
            resp = requests.get(ACCOUNTS, headers=self._headers())
            if resp.status_code == 200:
                for account in resp.json():
                    ret[account['securitiesAccount']['accountId']] = account
            else:
                raise Exception(resp.text)
        return ret
    def search(self, symbol, projection='symbol-search'):
        return requests.get(SEARCH,
                            headers=self._headers(),
                            params={'symbol': symbol,
                                    'projection': projection}).json()
    def instrument(self, cusip):
        return requests.get(INSTRUMENTS + str(cusip),
                            headers=self._headers()).json()
    def quote(self, symbol):
        return requests.get(QUOTES,
                            headers=self._headers(),
                            params={'symbol': symbol.upper()}).json()
    def history(self, symbol):
        return requests.get(HISTORY % symbol,
                            headers=self._headers()).json()
    def get_price_history(self, symbol, periodType='day', period='2', frequencyType='minute', frequency='1', needExtendedHoursData='false'):
        headers = self._headers()
        params = (
        ('apikey', 'DEARSOURABH99'),
        ('periodType', periodType),
        ('period', period),
        ('frequencyType', frequencyType),
        ('frequency', frequency),
        ('needExtendedHoursData', needExtendedHoursData),
        )
        res = requests.get(HISTORY % symbol, headers=headers, params=params).json()
        #print(res)
        if res['empty'] is True: return None
        df = pd.DataFrame(res['candles'])
        fcn = lambda x: datetime.datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d %H:%M:%S')
        df['datetime'] = pd.to_datetime(df['datetime'].map(fcn))
        return df.set_index('datetime')
    def option_chain(self, symbol, contractType, fromDate, toDate, strikeCount=40, includeQuotes='TRUE'):
        params = (
        #('apikey', 'DEARSOURABH99@AMER.OAUTHAP'),
        ('symbol', symbol),
        ('contractType', contractType),
        ('strikeCount', strikeCount),
        ('includeQuotes', includeQuotes),
        #('expMonth', 'SEP'),
        ('fromDate', fromDate),
        ('toDate', toDate),
        )
        #headers = {'Authorization': '',}
        headers = self._headers()
        return requests.get(OPTION_CHAINS,
                            headers=headers,
                            params=params).json()
    def get_strike_bid(self, symbol, symbolCount, contractType, fromDate, toDate, strikeCount=100, includeQuotes='TRUE'):
        d = self.option_chain(symbol,contractType,fromDate,toDate,strikeCount=strikeCount,includeQuotes='TRUE')
        if d['status']=='FAILED':
            print("option chain : \n",d)
        #print("option chain : \n",d)
        s = {}
        if contractType=='PUT':
            s = d["putExpDateMap"]
        else:
            s = d["callExpDateMap"]
        
        s1 = None
        for key in s:
            s1 = s[key]
            
        symbolData = pd.DataFrame(index=list(s1.keys()),columns=['Bid','OptionSymbol'])
        #print("symbolData : ",symbolData)
        for key in s1:
            symbolData.loc[key,'Bid'] = s1[key][symbolCount]['bid']
            symbolData.loc[key,'OptionSymbol'] = s1[key][symbolCount]['symbol']
        return symbolData
    def place_order(self, symbol=None, price=None, instruction=None, quantity=None):
        ORDERS = ACCOUNTS + str(self.accountIds) +'/orders'
        
        headers = self._headers()
        #headers = {
        #    'Authorization': 'Bearer ' + self._token,
        #    'Content-Type': 'application/json',
        #}
                      
        data = {
            #"tag" : tag, 
            #"orderId": 124421,
            "complexOrderStrategyType": "NONE",
            "orderType": "LIMIT",
            "session": "NORMAL",
            "price": price,
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
            {
            #"legId" : 3245,    
            "instruction": instruction,
            "quantity": quantity,
            "instrument": {
            "symbol": symbol,
            "assetType": "OPTION"
                }
            }
            ]
            }                    
       
        response = requests.post(ORDERS, headers=headers, data=json.dumps(data))
        #print(response.text)
        return response
    def get_orders_by_query(self, accountId, maxResults, status, date):
        body = BASE + 'orders'
        headers = {
            'Authorization': 'Bearer ' + self._token,
        }
        params1 = (
            ('accountId', accountId),
            ('maxResults', maxResults),
            ('status', status),
            ) 
        params2 = (
            ('accountId', accountId),
            ('maxResults', maxResults),
            ('fromEnteredTime', date),
            ('toEnteredTime', date),
            #('fromEnteredTime', '2018-09-08T12:01:07+0000'),
            #('toEnteredTime', '2018-09-08T14:01:07+0000'),
            ) 
        params = params2 if status == "ALL" else params1
        response = requests.get(body, headers=headers, params=params).json()
        return response
    def cancel_order(self, accountId, orderId):
        #https://api.tdameritrade.com/v1/accounts/865957580/orders/orderId
        body = BASE + 'accounts/' + accountId + '/orders/' + orderId
        headers = {
            'Authorization': 'Bearer ' + self._token,
        }
        #print(body)
        response = requests.delete(body, headers=headers)
        return response
    def cancel_working_orders(self, cancel_signal=False):
        date = datetime.date.today()
        if cancel_signal is True:
            orders = self.get_orders_by_query(ACCOUNT,30, "QUEUED", date)
            for order in orders:       
                orderId = order['orderId']
                print("Cancelling order : "+str(orderId))
                res = self.cancel_order(ACCOUNT, str(orderId))
                print(res.text)
    def cancel_working_orders_using_idseries(self, OrderIDSeries):
        #orders = self.get_orders_by_query(ACCOUNT,30, "QUEUED", date)
        for orderId in orderIDSeries:       
            print("Cancelling order Using ID in ID Series: "+str(orderId))
            res = self.cancel_order(ACCOUNT, str(orderId))
            print(res.text)    
    def remove_exp(self, num):
        return num.to_integral() if num == num.to_integral() else num.normalize()
    def get_order_by_id(self, OrderID):
        body1 = BASE + 'accounts/' + ACCOUNT + '/orders/'
        headers = {
            'Authorization': 'Bearer ' + self._token,
        }
        body = body1 + str(OrderID)
        response = requests.get(body, headers=headers).json()
        return response
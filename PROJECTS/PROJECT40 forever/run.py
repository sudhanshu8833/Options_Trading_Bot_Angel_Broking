# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from ta.trend import ADXIndicator, IchimokuIndicator, adx, EMAIndicator
from ta.volatility import BollingerBands, AverageTrueRange
from io import StringIO
import pyfolio as pf
import requests
import backtrader.feed as btfeeds
import backtrader.analyzers as btanalyzers
import backtrader as bt
from datetime import *
import sys
import os.path
import os
import datetime
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import math
import warnings
import time
import schedule
from ta.utils import dropna
from ta import add_all_ta_features
from datetime import date
from datetime import datetime
import pandas as pd
import ta
from time import sleep
from ib_insync import *
util.startLoop()
warnings.filterwarnings('ignore')
# display all df table, even when too long
pd.set_option('display.max_rows', None)
# Import math Library
# BACKTESTING
# pd.set_option('display.max_rows',None)# display all df table, even when too long
#sys.stdout = open("tradingLog.txt", 'a')

#fileName = open("tradingLog.txt","a")
# print('this is ap test Y',file =fileName)
# print('this is a test')#


# Connect to IBKR
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=12)  # paper trading


# %%
in_position = False
open_order = False
same_expiration = False
threshold = 34  # threshold at which a trend is considered - test 40,38 etc
adx_threshold = 20  # ADX threshold
# ADX max level after which, no mre trade entries. Possible reversal from here-out.
adx_max_level = 40
# ADX max level after which, a descending value leads to close of trades.
adx_close_level = 40
profit_taker = 50
profit_threshold = 40
reversal_threshold = 80  # threshold at which trend reversal ocurrs
dt = datetime.now()
Ophigh = 0  # opening range high
Oplow = 0  # Opening R low
prevhigh = 0  # previous day's high
prevlow = 0  # previous day's low
prevday_lastbar_high = 0  # last bar of previous day high
prevday_lastbar_low = 0  # lasbar of previous day low

# Backtesting data Only
pos = 0
num = 0
bp = 0
sp = 0
percentchange = []
initial_weight = np.array([100])
gains = 0
ng = 0
losses = 0
nl = 0
totalR = 1
dates = []


d = 100  # initialize the value of d, -divergence constant
D = 100  # initialize TRADE EXIT for level
DD = 100  # initialize
D50 = 100  # initialize 50 level TRADE EXIT for level

import sys

filename = sys.argv[1]

# %%


# ib.connect('127.0.0.1', 7496, clientId=12) # Real account trade
# subscribe to real time UNREALIZED P&L (put tading acc nr here. heart of profits. wait for 1 sec for data)
ib.reqPnL(account="DU4391061")

SPX = Index('SPX')
ib.qualifyContracts(SPX)
print(SPX)
ib.reqMarketDataType(1)
# marketDataType (int) One of:
# 1 = Live           - the default
# 2 = Frozen         - typically used for bid/ask prices after market close
# 3 = Delayed        - if the username does not have live market data subscriptions
# 4 = Delayed frozen - combination of types 2 & 3

#Request market data for symbol to get current traded price - Requesting a ticker can take up to 11 seconds.#
market_data = ib.reqMktData(SPX, '', False, False)
print(market_data)
ib.sleep(0.1)  # Wait until data is in.
SPXValue = market_data.last  # current price of equity
print(SPXValue)  # current price of symbol
# The following request fetches a list of option chains:
#chains = ib.reqSecDefOptParams(SPXValue.symbol(str), '', SPXValue.secType, SPXValue.conId)
# values got from *- print(SPX)
chains = ib.reqSecDefOptParams('SPX', '', 'IND', '416904')

#print(util.df(chains ))

# These are four option chains that differ in exchange and tradingClass. The latter is 'SPX' for the monthly and 'SPXW' for the weekly options.
# Note that the weekly expiries are disjoint from the monthly ones, so when interested in the weekly options the monthly options can be added as well.
# In this case we're only interested in the weekly (infact - daily) options trading on SMART:

# every 2 days expiration (Mon, Wed, Fri)
chain = next(c for c in chains if c.tradingClass ==
             'SPXW' and c.exchange == 'SMART')
chain2 = next(c for c in chains if c.tradingClass ==
              'SPX' and c.exchange == 'SMART')  # Monthly expiration (Tue,Thur)

# What we have here is the full matrix of expirations x strikes. From this we can build all the option contracts that meet our conditions:

chains = ib.reqSecDefOptParams(SPX.symbol, '', SPX.secType, SPX.conId)


# Sort the expiration contracts and choose the last one, usually today's or 1 day, or 2 days - but last
SPXP_expirations = sorted(exp for exp in chain.expirations)[:2]
# Sort the expiration contracts and choose the last one, usually today's or 1 day, or 2 days - but last
SPX_expirations = sorted(exp for exp in chain2.expirations)[:2]
if SPXP_expirations[:1] == SPXP_expirations[:1]:
    print("Na")
    same_expiration = True
else:
    print("yea")
    same_expiration = False
# Merge contracts with different expirations from different classes(SPXP & SPX)
# merge contracts with diff expirations from SPXP & SPX tradingClass
SPXP_expirations.extend(SPX_expirations)
# ['20220124', '20220126', '20220217', '20220317']
print("expirations from all tradingClass : ", SPXP_expirations)
expirations = SPXP_expirations[:1]
# expirations = sorted(exp for exp in chain.expirations)[:1] #Sort the expiration contracts and choose the last one, usually today's or 1 day, or 2 days - but last
print("Most recent expirations: ", expirations)
strikes = [strike for strike in chain.strikes
           if strike % 5 == 0
           and SPXValue - 5 < strike < SPXValue + 5]  # choose closest strike ITM
# and 14425 - 5 < strike < 14425 + 5] # Manual add for testing, on weekends with no display of punderlying price infor
print("strikes: ", strikes)

# expirations = sorted(exp for exp in chain.expirations)[:1] #Sort the expiration contracts and choose the last one, usually today's or 1 day, or 2 days - but last
#print("expirations: ",expirations)

# ********************************************************************************************
# Most recent Contract Info
# PUTS


def put_contract():
    # rights = ['P', 'C'] # where to specify whether just PUTS or Call, or Both contracts
    rights = ['P']
    # print(expirations)
    if same_expiration == True:
        p_contracts = [Option('SPX', expiration, strike, right, 'SMART', tradingClass='SPXW')
                       for right in rights
                       for expiration in expirations
                       for strike in strikes]
    else:
        p_contracts = [Option('SPX', expiration, strike, right, 'SMART')
                       for right in rights
                       for expiration in expirations
                       for strike in strikes]
#        print(strikes)
    p_contracts = ib.qualifyContracts(*p_contracts)
    return p_contracts[0]
# CALLS


def call_contract():
    # rights = ['P', 'C'] # where to specify whether just PUTS or Call, or Both contracts
    rights = ['C']
    # print(expirations)
    if same_expiration == True:
        c_contracts = [Option('SPX', expiration, strike, right, 'SMART', tradingClass='SPXW')
                       for right in rights
                       for expiration in expirations
                       for strike in strikes]
    else:
        c_contracts = [Option('SPX', expiration, strike, right, 'SMART')
                       for right in rights
                       for expiration in expirations
                       for strike in strikes]
#        print(strikes)
    c_contracts = ib.qualifyContracts(*c_contracts)
    return c_contracts[0]


#print("call_contract: ",call_contract())
# ********************************************************************************************
# Future (nextday) Contract Info
nextday_expirations = []
# Add 'next day contract to list' to the list
nextday_expirations.append(SPXP_expirations[1])
# PUTS


def nextday_put_contract():
    # rights = ['P', 'C'] # where to specify whether just PUTS or Call, or Both contracts
    rights = ['P']
    # print(expirations)
    p_contracts = [Option('SPX', expiration, strike, right, 'SMART')
                   for right in rights
                   for expiration in nextday_expirations
                   for strike in strikes]
#        print(strikes)
    p_contracts = ib.qualifyContracts(*p_contracts)
    return p_contracts[0]
# CALLS


def nextday_call_contract():
    # rights = ['P', 'C'] # where to specify whether just PUTS or Call, or Both contracts
    rights = ['C']
    # print(expirations)
    c_contracts = [Option('SPX', expiration, strike, right, 'SMART')
                   for right in rights
                   for expiration in nextday_expirations
                   for strike in strikes]
#        print(strikes)
    c_contracts = ib.qualifyContracts(*c_contracts)
    return c_contracts[0]
# ********************************************************************************************
#print("nextday_put_contract: ",nextday_put_contract())
#print("nextday_call_contract: ",nextday_call_contract())


# Market Order - Modifying orders
SPX_open_mkt_order_mod = Order(
    orderId=0, orderType='MKT', action='BUY', totalQuantity=1, auxPrice=0.01)
SPX_close_mkt_order_mod = Order(
    orderId=0, orderType='MKT', action='SELL', totalQuantity=1, auxPrice=0.01)

# Snap Mid Order Type
# orderId =0 first order, so it can be refereced and cancelled
SPX_open_snap_mid_order = Order(
    orderId=0, orderType='SNAP MID', action='BUY', totalQuantity=1, auxPrice=0.05)
SPX_close_snap_mid_order = Order(
    orderId=0, orderType='SNAP MID', action='SELL', totalQuantity=1, auxPrice=0.05)

# LimitOrder Type -Used for testing
SPX_close_limit_order = Order(orderId=0, orderType='LMT',
                              action='BUY', totalQuantity=2, lmtPrice=3.1, auxPrice=0.05)


# Defining Time
def current_time():
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%H:%M:%S")
    #print(f"Current time is {current_time}")
    return current_time


def close_time():
    # Just TIME portion considered in calculating closing time
    close_datetime = datetime.strptime(
        '2021-12-17 13:57:00', '%Y-%m-%d %H:%M:%S')
    # close_datetime = datetime.strptime('2021-12-17 16:59:00', '%Y-%m-%d %H:%M:%S')# for testing closing times
    close_time = close_datetime.strftime("%H:%M:%S")  # 13:57:00
    #print(f"Close time is {close_time}")
    return close_time


def open_time():
    # Just TIME portion considered in calculating closing time
    open_datetime = datetime.strptime(
        '2021-12-17 07:30:03', '%Y-%m-%d %H:%M:%S')
    # close_datetime = datetime.strptime('2021-12-17 16:59:00', '%Y-%m-%d %H:%M:%S')# for testing closing times
    open_time = open_datetime.strftime("%H:%M:%S")  # 13:57:00
    #print(f"Open time is {open_time}")
    return open_time


def end_order_time():
    # Just TIME portion considered in calculating closing time
    end_order_datetime = datetime.strptime(
        '2021-12-17 13:55:00', '%Y-%m-%d %H:%M:%S')
    # close_datetime = datetime.strptime('2021-12-17 16:59:00', '%Y-%m-%d %H:%M:%S')# for testing closing times
    end_order_time = end_order_datetime.strftime("%H:%M:%S")  # 13:50:00
    #print(f"Open time is {open_time}")
    return end_order_time


def out_of_open_time():  # end of morning time with random volatility
    # Just TIME portion considered in calculating closing time
    out_of_open_datetime = datetime.strptime(
        '2021-12-17 08:05:00', '%Y-%m-%d %H:%M:%S')
    # close_datetime = datetime.strptime('2021-12-17 16:59:00', '%Y-%m-%d %H:%M:%S')# for testing closing times
    out_of_open_time = out_of_open_datetime.strftime("%H:%M:%S")  # 13:50:00
    #print(f"Open time is {open_time}")
    return out_of_open_time


# def dmi_trend(df):
    # By default, there is no open trade
positions = ib.positions()  # A list of positions, according to IB
for position in positions:
    in_position = True  # True There is an open trade before start of session
    print('There is an open position. Look 4 sell opportunities...')
    contract = Contract(conId=position.contract.conId)
    ib.qualifyContracts(contract)
    print('Current contract in position')
    print(contract)

# def in_position():
#     positions = ib.positions()  # A list of positions, according to IB
#     for position in positions:
#         if position in positions:
#             in_position = True  #True There is an open trade before start of session
#         else:
#              in_position = False
    # return in_position


# On reconnect Cancel open order and place market order to close position
def cancel_openOrders():
    All_Orders = ib.openOrders()
    for order in ib.openOrders():
        ib.cancelOrder(order)  # cancel order t
        ib.sleep(0.0001)
        positions = ib.positions()  # A list of positions, according to IB
        for position in positions:
            contract = Contract(conId=position.contract.conId)
            ib.qualifyContracts(contract)
            # Modify order to snap BUY call order
            close_trade = ib.placeOrder(contract, SPX_close_mkt_order_mod)
            print("pending open order closed, mkt order submitted")
            ib.sleep(0.001)
            in_position = False


# Cancel open orders on re-connect which were not submitted on disconnect
cancel_openOrders()

# ib.placeOrder(call_contract(), SPX_open_snap_mid_order)
# print('testing over')


# %%
def candle():  # Data frame build
    global d
    global bp
    global sp
    global pos
    global Ophigh
    global Oplow
    global prevhigh
    global prevlow
    global prevday_lastbar_high
    global prevday_lastbar_low

    bars = ib.reqHistoricalData(
        SPX,
        endDateTime='',
        # 1 D after testing, this is number to go (55 bars = 1 D (5 mins)) ADX need 26+24 bars
        durationStr='13800 S',
        barSizeSetting='1 min',
        whatToShow='TRADES',
        useRTH=True,
        keepUpToDate=True,
    )
#print(util.df(bars ))

    df = pd.DataFrame(bars)
    # print(df.tail(10))
    last_row_index = len(df.index)-1
    previous_row_index = last_row_index-1
    ib.sleep(0.001)

    # 7:30 today (on a 2D duration bar)

#df['timesstamp'] = pd.to_datetime(df['timestamp'],unit='ms')
# print(df)

# INDICATORS
# ********************************************************************************************
# definition    - > BollingerBands(close: pandas.core.series.Series, window: int = 20, window_dev: int = 2, fillna: bool = False)
# Intepretation - > BollingerBands(close=df["Close"], window=20, window_dev=2)

# definition    - > ADXIndicator(high: pandas.core.series.Series, low: pandas.core.series.Series, close: pandas.core.series.Series, window: int = 14, fillna: bool = False)
# Intepretation - > ADXIndicator(high=df["high"],low=df["low"],close=df["close"],window=4)

# definition    - > IchimokuIndicator(high: pandas.core.series.Series, low: pandas.core.series.Series, window1: int = 9, window2: int = 26, window3: int = 52, visual: bool = False, fillna: bool = False)
# Intepretation - > IchimokuIndicator(high=df["high"],low=df["low"])

# definition    - > adx(high, low, close, window=14, fillna=False)
# Intepretation - > adx(high=df["high"],low=df["low"],close=df["close"])

# definition    - > EMAIndicator(close: pandas.core.series.Series, window: int = 14, fillna: bool = False)
# Intepretation - > EMAIndicator(close=df["close"]

# Intepretation - > AverageTrueRange(high=df["high"],low=df["low"],close=df["close"],window=20)
# ********************************************************************************************
    # df['D50_P'] = False #initializing zone of take profit downtrend
    # df['D50_C'] = False #initializing zone of take profit uptrend
    # df['Rev50'] = False # Ininitalize daily profit
    # Ininitialize exit when price very high, likely out of bollinger band - DMIPlus/DMIMinus >=90
    df['BB_exit'] = False
    df['brkout'] = False  # Ininitalize ORB Opening Range Breakout
    df['gap'] = 0  # Ininitalize max take profit limit of the session
    df['maxlimit'] = False  # Ininitalize max take profit limit of the session
    df['maxlimit2'] = False  # Ininitalize max take profit limit of the session
    # Ininitalize parameter to calculate max session take profit
    df['profits'] = False

    # Initialize Bollinger Bands Indicator
    bb_indicator = BollingerBands(df['close'])
    df['upper_band'] = bb_indicator.bollinger_hband()
    df['lower_band'] = bb_indicator.bollinger_lband()
    atr_indicator = AverageTrueRange(
        high=df["high"], low=df["low"], close=df["close"], window=5)
    #df['bb_moving_avg'] = bb_indicator.bollinger_mavg()
    df['D'] = False  # High risk no enter regions, exiting BB
    df['down'] = False  # Ininitialize down signals with ADX below threshold
    df['up'] = False  # Ininitialize uptrend signals with ADX below threshold
    EMA_Indicator = EMAIndicator(close=df["close"], window=34)
    df['ema_34'] = EMA_Indicator.ema_indicator()
    df['atr'] = atr_indicator.average_true_range()

   # Initialize Average Directional Movement Index (ADX) Indicator
    #df['adx'] = adx(high=df["high"],low=df["low"],close=df["close"],window=14)

    # Initialize  Directional Movement Indicator (DMI)  Indicator
    DMI_ndicator = ADXIndicator(
        high=df["high"], low=df["low"], close=df["close"], window=7)
    #adx_indicator = ADXIndicator(high=df["high"],low=df["low"],close=df["close"],window=14)
    df['DMIPlus'] = DMI_ndicator.adx_pos()
    df['DMIMinus'] = DMI_ndicator.adx_neg()
    #df['previous_close'] =df['close'].shift(1)
    df['tkprofit'] = False  # Ininitalize take profit to limit loss
    df['adx'] = adx(high=df["high"], low=df["low"],
                    close=df["close"], window=14)
    df['cndl'] = Revsignal1(df)  # candlestick pattern retracement with ATR
    df['cndl2'] = Revsignal2(df)  # candlestick pattern retracement without ATR
    df['In_Uptrend'] = False  # Ininitialize Uptrend signals
    df['In_Downtrend'] = False  # Ininitialize Downtrend signals
    df['sgnalB'] = 0  # Ininitialize long signals
    df['sgnalS'] = 0  # Ininitialize shortSignals

    #df.replace(np.nan, 0)
    # df.dropna(inplace=True)


# print(df)

# setting trend conditions
    for current in range(1, len(df.index)):
        previous = current-1
        previous03 = current-2
        previous04 = current-3
        previous05 = current-4
        # date manipulation
        dt = df['date'][current] + timedelta(minutes=25)
        today = date.today()
        # YY/mm/dd
        dt_today = today.strftime("%Y%m%d")  # in format 20220225
        today_dt_curr = df['date'][current]
        today_dt = today_dt_curr.strftime("%Y%m%d")

# ********************************************************************************************
# setting uptrend - CALL conditions
# ********************************************************************************************

#                  Main Condition DMI Indicator -(Not included re entry into market upto ADX 40 level)

        # if df['DMIPlus'][current] > df['DMIMinus'][current]:            #Opening market defies all exceptions-DMIPlus > DMIMinus
        #   if df['date'][current].strftime("%H:%M:%S") == "07:30:00":
        #     if  df['adx'] [current] > df['adx'] [previous]: # rising ADX signify a good signal
        #     #if df['DMIPlus'][current]>threshold:                                #DMIPlus > threshold
        #         df['In_Uptrend'][current] = True

        if df['DMIPlus'][current] > df['DMIMinus'][current]:  # DMIPlus > DMIMinus
            if df['adx'][current] > df['adx'][previous] and df['adx'][previous] > df['adx'][previous03] and\
                    df['adx'][previous03] > df['adx'][previous04]:  # rising ADX, enter at 3rd candle of continuoes uptrend of the ADX line
                if df['DMIPlus'][current] > df['DMIPlus'][previous]:  # rising slope of DMIPlus
                    # price must be greater than 34 EMA for uptrend
                    if df['close'][current] > df['ema_34'][current]:
                        df['In_Uptrend'][current] = True

        elif df['DMIPlus'][current] < df['DMIMinus'][current]:
            df['In_Uptrend'][current] = False
        else:
            # Maintain default
            df['In_Uptrend'][current] = df['In_Uptrend'][previous]

# # 1 - Extend the signal to all bars when first condition met
        if df['DMIPlus'][current] > df['DMIMinus'][current]:  # DMI+ greater then DMI-
            if df['In_Uptrend'][previous] == True:
                df['In_Uptrend'][current] = True

# ********************************************************************************************
# setting Downtrend - PUT conditions (same condions as above but reversed)
# ********************************************************************************************
#                  Main Condition for PUT
        # if df['DMIMinus'][current] > df['DMIPlus'][current]:            #Opening market defies all exceptions-DMIPlus > DMIMinus
        #   if df['date'][current].strftime("%H:%M:%S") == "07:30:00":
        #       if  df['adx'] [current] > df['adx'] [previous]: # rising ADX signify a good signal
        #     #if df['DMIPlus'][current]>threshold:                                #DMIPlus > threshold
        #         df['In_Downtrend'][current] = True

        if df['DMIMinus'][current] > df['DMIPlus'][current]:
            if df['adx'][current] > df['adx'][previous] and df['adx'][previous] > df['adx'][previous03] and\
                    df['adx'][previous03] > df['adx'][previous04]:  # rising ADX, enter at 3rd candle of continuoes uptrend of the ADX line
                if df['DMIMinus'][current] > df['DMIMinus'][previous]:  # rising slope of DMIMinus
                    # price must be less than 34 EMA for downtrend
                    if df['close'][current] < df['ema_34'][current]:
                        df['In_Downtrend'][current] = True

        elif df['DMIMinus'][current] < df['DMIPlus'][current]:
            # if df['DMIPlus'][current]>threshold:
            # by default everything is false, so this line was unnecessary.
            df['In_Downtrend'][current] = False
        else:
            df['In_Downtrend'][current] = df['In_Downtrend'][previous]

# # 1 - Extend the signal to all bars when first condition met
        if df['In_Downtrend'][previous] == True:
            if df['DMIMinus'][current] > df['DMIPlus'][current]:  # DMI- greater then DMI+
                df['In_Downtrend'][current] = True

# ********************************************************************************************

# EARLY PROFIT TARGET DMI+/DMI* ABOVE 50
 # - Exceptions - TRUE - Exiting bollinger band (lower/upper)

        if df['close'][current] > df['upper_band'][current] or df['close'][current] < df['lower_band'][current]:
            df['BB_exit'][current] = True

        if df['BB_exit'][current] == True:
            if df['BB_exit'][previous] == False and df['BB_exit'][previous03] == False and df['BB_exit'][previous04] == False:
                df['D'][current] = True

            # if (df['low'][current] > df['high'][previous])  :
            # df['gap'][current]  = 1 # gap up

            # if (df['high'][current] < df['low'][previous])  :
            # df['gap'][current]  = -1 # gap down


# 8 - Trend Reversal - breakout- PUT
        if df['adx'][current] > df['adx'][previous]:
            if (df['high'][current] < df['low'][previous] or df['In_Downtrend'][current] == True):
                if df['date'][current].strftime("%H:%M:%S") == "07:30:00":
                    df['brkout'][current] = True

        if df['brkout'][previous] == True:
            if df['In_Downtrend'][current] == True or (df['high'][previous] < df['low'][previous03] or df['high'][previous03] < df['low'][previous04]):
                df['brkout'][current] = True

        if df['brkout'][previous] == True:
            if df['In_Downtrend'][current] == True or (df['adx'][current] > df['adx'][previous]):
                df['brkout'][current] = True

        if df['In_Downtrend'][current] == False and df['In_Downtrend'][previous] == True:
            if df['brkout'][previous] == True:
                df['brkout'][current] = False

        if df['In_Downtrend'][current] == True and df['In_Uptrend'][previous] == True:
            if df['date'][current].strftime("%H:%M:%S") != "07:30:00":
                df['brkout'][current] = False

# # 8 - Trend Reversal - breakout- Call
        if df['adx'][current] > df['adx'][previous]:
            if (df['In_Uptrend'][current] == True or df['low'][current] > df['high'][previous]):
                if df['date'][current].strftime("%H:%M:%S") == "07:30:00":
                    df['brkout'][current] = True

        if df['brkout'][previous] == True:
            if df['In_Uptrend'][current] == True or (df['low'][previous] > df['high'][previous03] or df['low'][previous03] > df['high'][previous04]):
                df['brkout'][current] = True

        if df['brkout'][previous] == True:
            if df['In_Uptrend'][current] == True or (df['adx'][current] > df['adx'][previous]):
                df['brkout'][current] = True

        if df['In_Uptrend'][current] == False and df['In_Uptrend'][previous] == True:
            if df['brkout'][previous] == True:
                df['brkout'][current] = False

        if df['In_Uptrend'][current] == True and df['In_Downtrend'][previous] == True:
            if df['date'][current].strftime("%H:%M:%S") != "07:30:00":
                df['brkout'][current] = False

# ********************************************************************************************
# # 8 - EARLY PROFIT TAKERS - breakout- Call
        if df['In_Uptrend'][current] == True and df['brkout'][current] == True:
            # Only time portion of datetime is evaluated
            if current_time() > datetime.strptime('2021-12-17 07:35:00', '%Y-%m-%d %H:%M:%S').strftime("%H:%M:%S"):
                # 3rd bar ago green or 2nd bar ago green  ...
                if (df['close'][previous03] > df['open'][previous03] or df['close'][previous] > df['open'][previous]):
                    if df['DMIPlus'][current] < df['DMIPlus'][previous] and\
                       df['DMIPlus'][previous] > df['DMIPlus'][previous03]:  # current DMI- up downtrending and previous DMI- up trending
                        # if (df['open'][current] > df['high'][previous] ) :#Ophigh
                        df['tkprofit'][current] = True

# # 8 - EARLY PROFIT TAKERS - - Call
        # if df['In_Uptrend'][current]==True:
        if df['DMIPlus'][previous] >= profit_taker:  # profit_taker: DMI >=50
            # if df['open'][current]>df['close'][current]:# current RED bar - trending DOWN
            # if df['close'][previous] >df['open'][previous] :# green bar 1 bar ago ...
            # current DMI- up downtrending and previous DMI- up trending
            if df['DMIPlus'][current] < df['DMIPlus'][previous]:
                df['tkprofit'][current] = True

# # 8 - EARLY PROFIT TAKERS - - Call Keep taking profits solong as this is true
        if df['tkprofit'][previous] == True and df['brkout'][current] == True:
            # or (df['DMIPlus'][current]>df['DMIMinus'][current]):
            if df['In_Uptrend'][current] == True:
                df['tkprofit'][current] = True

        if df['In_Uptrend'][current] == False and df['In_Uptrend'][previous] == True or\
           (df['DMIMinus'][current] > df['DMIPlus'][current] and df['DMIPlus'][previous] > df['DMIMinus'][previous]):
            if df['tkprofit'][previous] == True:
                df['tkprofit'][current] = False
# ********************************************************************************************
# Defining the Max take profit region
# ********************************************************************************************
# # 8 - MAX PROFIT REACHED - - Call
        if df['tkprofit'][previous] == True:
            df['profits'][current] = True

        if df['profits'][previous] == True:
            if df['In_Uptrend'][current] == True:
                df['profits'][current] = True
# ********************************************************************************************
# # 8 - MAX PROFIT REACHED - - Call
        if df['profits'][current] == True:
            if df['In_Uptrend'][current] == True:
                if df['adx'][current] > adx_max_level:
                    if df['DMIPlus'][current] < df['DMIPlus'][previous]:  # descending trend
                        df['maxlimit'][current] = True
# Extend to all bars
        if df['maxlimit'][previous] == True:
            if df['In_Uptrend'][current] == True:
                df['maxlimit'][current] = True
# ********************************************************************************************
# ********************************************************************************************
# # 8 - EARLY PROFIT TAKERS - breakout- Put
        if df['In_Downtrend'][current] == True and df['brkout'][current] == True:
            # Only time portion of datetime is evaluated
            if current_time() > datetime.strptime('2021-12-17 07:35:00', '%Y-%m-%d %H:%M:%S').strftime("%H:%M:%S"):
                # if (df['close'][previous03] >df['open'][previous03] or df['close'][previous] >df['open'][previous]):# 3rd bar ago green or 2nd bar ago green ......
                if df['DMIMinus'][current] < df['DMIMinus'][previous] and\
                   df['DMIMinus'][previous] > df['DMIMinus'][previous03]:  # current DMI- up downtrending and previous DMI- up trending
                    # if (df['close'][current] > Ophigh) or (df['high'][current] > Ophigh):
                    df['tkprofit'][current] = True

# # 8 - EARLY PROFIT TAKERS - - Put
        if df['DMIMinus'][previous] >= profit_taker:  # profit_taker: DMI >=50
            # if df['open'][previous] >df['close'][previous] :# green bar 1 bar ago ...
            # current DMI- up downtrending and previous DMI- up trending
            if df['DMIMinus'][current] < df['DMIMinus'][previous]:
                df['tkprofit'][current] = True

# # 8 - EARLY PROFIT TAKERS - - Put Keep taking profits solong as this is true
        if df['tkprofit'][previous] == True and df['brkout'][current] == True:
            # or (df['DMIMinus'][current]>df['DMIPlus'][current]):
            if df['In_Downtrend'][current] == True:
                df['tkprofit'][current] = True

        if df['In_Downtrend'][current] == False and df['In_Downtrend'][previous] == True or\
           (df['DMIPlus'][current] > df['DMIMinus'][current] and df['DMIMinus'][previous] > df['DMIPlus'][previous]):
            if df['tkprofit'][previous] == True:
                df['tkprofit'][current] = False
# ********************************************************************************************
# Defining the Max take profit region
# ********************************************************************************************
# # 8 - MAX PROFIT REACHED - - Call
        if df['tkprofit'][previous] == True:
            df['profits'][current] = True

        if df['profits'][previous] == True:
            if df['In_Downtrend'][current] == True:
                df['profits'][current] = True
# ********************************************************************************************
# # 8 - MAX PROFIT REACHED - - Call
        if df['profits'][current] == True:
            if df['In_Downtrend'][current] == True:
                if df['adx'][current] > adx_max_level:
                    if df['DMIMinus'][current] < df['DMIMinus'][previous]:  # descending trend
                        df['maxlimit'][current] = True

# Extend to all bars
        if df['maxlimit'][previous] == True:
            if df['In_Downtrend'][current] == True:
                df['maxlimit'][current] = True

# Stop loss if still in trade

        if df['maxlimit'][current] == True:
            if df['adx'][current] < df['adx'][previous]:
                df['tkprofit'][current] = True

# AVOID GAP UP/DOWN TRADE CONTINUATION OUTSIDE BOLLINGER BAND - Call/Put
        if (df['low'][current] > df['high'][previous]):
            df['gap'][current] = 1  # gap up

        if (df['high'][current] < df['low'][previous]):
            df['gap'][current] = -1  # gap up


# ********************************************************************************************
####################################################################################
#           BACKTEST VARIOUS SIGNALS SCENARIOS HERE (buy = 1, exit=-1, no signal = 0)
#           Comment the strategy block to backtest the signal of a particular strategy
####################################################################################
# -------------------------------CALL---------------------------


# Strategy 1 - Original Crossover at threshhold (34) Strategy
####################################################################################
        # if df['In_Uptrend'][current]==True and  df['In_Uptrend'][previous]==False : #DMI+ greater then DMI-
        #     df['sgnalB'][current] = 1# buy long signal
        #     pos = 1

        # if df['In_Uptrend'][current]==False and  df['In_Uptrend'][previous]==True and pos == 1: #DMI+ greater then DMI-
        #             df['sgnalB'][current] = -1# exit long signal
        #             pos = 0
####################################################################################
# Strategy 2 - Early profit at DMI>=50
        if df['In_Uptrend'][current] == True and df['In_Uptrend'][previous] == False:  # DMI+ greater then DMI-
            df['sgnalB'][current] = 1  # buy long signal
            pos = 1

        elif df['In_Uptrend'][current] == True and pos == 1:
            if df['tkprofit'][current] == True and df['tkprofit'][previous] == False:  # EARLY TAKE PROFIT
                if df['DMIPlus'][current] < df['DMIPlus'][previous]:   # current DMI+ down downtrending
                    df['sgnalB'][current] = -1  # exit long signal
                    pos = 0

        elif df['In_Uptrend'][current] == True:
            if df['tkprofit'][current] == True and df['DMIPlus'][current] > df['DMIPlus'][previous] and\
                    df['DMIPlus'][previous] < df['DMIPlus'][previous03] and pos == 0:
                df['sgnalB'][current] = 1
                pos = 1

        if df['In_Uptrend'][current] == True:
            if df['tkprofit'][current] == True and df['tkprofit'][previous] == True and df['DMIPlus'][current] < df['DMIPlus'][previous] and\
                    df['DMIPlus'][previous] > df['DMIPlus'][previous03] and pos == 1:
                df['sgnalB'][current] = -1  # exit long signal
                pos = 0

        if df['In_Uptrend'][current] == False and df['In_Uptrend'][previous] == True and pos == 1:  # DMI+ greater then DMI-
            if df['tkprofit'][current] == False:
                df['sgnalB'][current] = -1  # exit long signal
                pos = 0

 ####################################################################################
# -------------------------------PUT---------------------------


# Strategy 1 - Original Crossover at threshhold (34) Strategy
####################################################################################
        # if df['In_Downtrend'][current]==True and  df['In_Downtrend'][previous]==False : #DMI+ greater then DMI-
        #     df['sgnalS'][current] = 1# buy long signal
        #     pos = 1

        # if df['In_Downtrend'][current]==False and  df['In_Downtrend'][previous]==True and pos == 1: #DMI+ greater then DMI-
        #             df['sgnalS'][current] = -1# exit long signal
        #             pos == 0
####################################################################################
# Strategy 2 - Early profit at DMI>=50
        # DMI- greater then DMI+
        if df['In_Downtrend'][current] == True and df['In_Downtrend'][previous] == False:
            df['sgnalS'][current] = 1  # buy long signal
            pos = 1

        elif df['In_Downtrend'][current] == True and pos == 1:
            if df['tkprofit'][current] == True and df['tkprofit'][previous] == False:  # EARLY TAKE PROFIT
                # current DMI+ down downtrending
                if df['DMIMinus'][current] < df['DMIMinus'][previous]:
                    df['sgnalS'][current] = -1  # exit long signal
                    pos = 0

        elif df['In_Downtrend'][current] == True:
            if df['tkprofit'][current] == True and df['DMIMinus'][current] > df['DMIMinus'][previous] and\
                    df['DMIMinus'][previous] < df['DMIMinus'][previous03] and pos == 0:
                df['sgnalS'][current] = 1
                pos = 1

        if df['In_Downtrend'][current] == True:
            if df['tkprofit'][current] == True and df['tkprofit'][previous] == True and df['DMIMinus'][current] < df['DMIMinus'][previous] and\
                    df['DMIMinus'][previous] > df['DMIMinus'][previous03] and pos == 1:
                df['sgnalS'][current] = -1  # exit long signal
                pos = 0

        if df['In_Downtrend'][current] == False and df['In_Downtrend'][previous] == True and pos == 1:  # DMI+ greater then DMI-
            if df['tkprofit'][current] == False:
                df['sgnalS'][current] = -1  # buy long signal
                pos = 0

 ####################################################################################


# ****************************************************************************************
# #FOR Testing only - simulate CALL signal
#         last_row_index = len(df.index)-1
#         previous_row_index = last_row_index-1

#         df['In_Uptrend'][previous_row_index] = False   # True -  force a BUY trade for testing - true
#         df['In_Uptrend'][last_row_index]     = True  # False  -  force a SELL trade for testing -
#         df['BB_exit'][last_row_index]        = True
# # #****************************************************************************************
# # #FOR Testing only - simulate PUT signal
#         df['In_Downtrend'][previous_row_index] = False    # True -  force a BUY trade for testing - true
#         df['In_Downtrend'][last_row_index]     = True   # False  -  force a SELL trade for testing -
#         df['BB_exit'][last_row_index]          = True
# ****************************************************************************************

    # data saved as csv file in same folder as code,to be used as input to backtest
    df.to_csv("spx.csv")
    # updatesignal()

    print(df)

    # print(df[11:-1])
    # return df[:-1] # only closed bars, ignore the last forming bar
    return df  # early prediction, all bars includig forming

# # ############################################################################################################################
# # # Hammer and Shooting Star Candlestick Pattern - for special take profit signals with ATR
# # ############################################################################################################################


def Revsignal1(df):
    # df.dropna()
    #df.reset_index(drop=True, inplace=True)

    length = len(df)
    high = list(df['high'])
    low = list(df['low'])
    close = list(df['close'])
    open = list(df['open'])
    signal = [0] * length
    highdiff = [0] * length
    lowdiff = [0] * length
    bodydiff = [0] * length
    ratio1 = [0] * length
    ratio2 = [0] * length

    for row in range(0, length):

        # length of high/long tail in downtrend shooting star candle
        highdiff[row] = high[row]-max(open[row], close[row])
        # body of shooting star candle
        bodydiff[row] = abs(open[row]-close[row])
        # make sure there is not zero (i.e. open price = lose price)
        if bodydiff[row] < 0.002:
            bodydiff[row] = 0.002
        # length of the small tail  below the body of the candlestick
        lowdiff[row] = min(open[row], close[row])-low[row]
        ratio1[row] = highdiff[row]/bodydiff[row]
        ratio2[row] = lowdiff[row]/bodydiff[row]

        # Shooting Star
        #  |
        # _|_
        # |__|
        # |
        #
        # high tail longer than 2.5, low tail less than 1/3
        if (ratio1[row] > 0.01 and bodydiff[row] >= 0.75*df['atr'][row] and df['close'][row] > df['open'][row]):
            # if (ratio1[row]>2.5 and lowdiff[row]<0.3*highdiff[row] and bodydiff[row]>0.03): # high tail longer than 2.5, low tail less than 1/3
            signal[row] = 1

        # hammer
        # _|_
        # |__|
        # |
        # |
        elif (ratio2[row] > 0.01 and bodydiff[row] >= 0.75*df['atr'][row] and df['open'][row] > df['close'][row]):
            # elif (ratio2[row]>0.4 and bodydiff[row]>0.03):
            signal[row] = 2
    return signal
# # ############################################################################################################################
# # # Hammer and Shooting Star Candlestick Pattern - for special take profit signals without ATR
# # ############################################################################################################################


def Revsignal2(df):
    # df.dropna()
    #df.reset_index(drop=True, inplace=True)

    length = len(df)
    high = list(df['high'])
    low = list(df['low'])
    close = list(df['close'])
    open = list(df['open'])
    signal = [0] * length
    highdiff = [0] * length
    lowdiff = [0] * length
    bodydiff = [0] * length
    ratio1 = [0] * length
    ratio2 = [0] * length

    for row in range(0, length):

        # length of high/long tail in downtrend shooting star candle
        highdiff[row] = high[row]-max(open[row], close[row])
        # body of shooting star candle
        bodydiff[row] = abs(open[row]-close[row])
        # make sure there is not zero (i.e. open price = lose price)
        if bodydiff[row] < 0.002:
            bodydiff[row] = 0.002
        # length of the small tail  below the body of the candlestick
        lowdiff[row] = min(open[row], close[row])-low[row]
        ratio1[row] = highdiff[row]/bodydiff[row]
        ratio2[row] = lowdiff[row]/bodydiff[row]

        # Shooting Star
        #  |
        # _|_
        # |__|
        # |
        #
        # high tail longer than 2.5, low tail less than 1/3
        if (ratio1[row] > 0.01 and bodydiff[row] > 0.002 and df['close'][row] > df['open'][row]):
            # if (ratio1[row]>2.5 and lowdiff[row]<0.3*highdiff[row] and bodydiff[row]>0.03): # high tail longer than 2.5, low tail less than 1/3
            signal[row] = 1

        # hammer
        # _|_
        # |__|
        # |
        # |
        elif (ratio2[row] > 0.01 and bodydiff[row] > 0.002 and df['open'][row] > df['close'][row]):
            # elif (ratio2[row]>0.4 and bodydiff[row]>0.03):
            signal[row] = 2
    return signal
# # ############################################################################################################################
# # # Print Message to file - Trade Logs
# # ############################################################################################################################


def print2file(a="print on the screen"):
    df = candle()
    # with open("tradingLog.txt","a") as fileName:
    # fully qualify path with double quotes
    with open("C:\\Users\peter\\OneDrive\\Desktop\\Trade_project\\interactive-brokers-api\\interactive-brokers-demo\\tradingLog.txt", "a") as fileName:

        print('{}| {}|DMIPlus: {}| DMIMinus: {}| Current time: {}|'.format(df['date'].iloc[-1].strftime(
            "%Y-%m-%d %H:%M:%S"), a, df['DMIPlus'].iloc[-1], df['DMIMinus'].iloc[-1], current_time()), file=fileName)
    return


# ib.sleep(0.001)
#print2file("print on the screen yo")
#print2file("print on the screen using fileName.write")
############################################################################################################################
# Enter A position before entering the MAIN LOOP (for quick execution)
############################################################################################################################
ib.sleep(0.001)
df = candle()

if in_position == False:
    if current_time() < end_order_time() and current_time() >= open_time():
        if df['In_Uptrend'].iloc[-1] == True:
            if df['DMIPlus'].iloc[-1] > df['DMIPlus'].iloc[-2]:  # DMI+ uptrending
                if df['adx'].iloc[-1] > df['adx'].iloc[-2]:  # rising ADX signify a good signal
                    if df['close'].iloc[-1] > df['open'].iloc[-1]:  # a green bar - trending up
                        # no more new trades when ADX is above adx_max_level- Max take profit for the session is reached
                        if df['maxlimit'].iloc[-1] == False or df['maxlimit2'].iloc[-1] == False:

                            trade = ib.placeOrder(
                                call_contract(), SPX_open_snap_mid_order)
                            print("Call Order is Placed (SNAP MID)")
                            # print to file without PnL
                            print2file("Call Order is Placed (SNAP MID)")
                            # wait for, the logic for closing a trade 3 secs
                            ib.sleep(3)
                            print('1st sleep')
                            if trade.orderStatus.status != 'Filled':  # if first order type"SNAP MID" is not filled, then get ready
                                # cancel order
                                ib.cancelOrder(SPX_open_snap_mid_order)
                                ib.sleep(0.0001)
                                # Modify order, place market BUY Put order
                                trade = ib.placeOrder(
                                    call_contract(), SPX_open_mkt_order_mod)
                                print(trade)
                                in_position = True
                                print("CALL Order is Placed (MKT)")
                                # Print to file without PnL
                                print2file("CALL Order is Placed (MKT)")
                            else:
                                in_position = True
                                print(
                                    "1st-Already in CALL position (SNAP MID order successful), nothing to do...")
                                print2file(
                                    "1st-Already in CALL position (SNAP MID order successful), nothing to do...")


############################################################################################################################
        if df['In_Downtrend'].iloc[-1] == True:
            if df['DMIMinus'].iloc[-1] > df['DMIMinus'].iloc[-2]:  # DMI- downtrending
                if df['adx'].iloc[-1] > df['adx'].iloc[-2]:  # rising ADX signify a good signal
                    if df['open'].iloc[-1] > df['close'].iloc[-1]:  # a red bar - trending up
                        trade = ib.placeOrder(
                            put_contract(), SPX_open_snap_mid_order)
                        print("PUT Order is Placed (SNAP MID)")
                        print2file("PUT Order is Placed (SNAP MID)")
                        ib.sleep(3)
                        print('1st sleep')
                        if trade.orderStatus.status != 'Filled':  # if first order type"SNAP MID" is not filled, then get ready
                            # cancel order
                            ib.cancelOrder(SPX_open_snap_mid_order)
                            ib.sleep(0.0001)
                            # Modify order, place market BUY Put order
                            trade = ib.placeOrder(
                                put_contract(), SPX_open_mkt_order_mod)
                            print(trade)
                            in_position = True
                            print("PUT Order is Placed (MKT)")
                            print2file("PUT Order is Placed (MKT)")

                        else:
                            in_position = True
                            print(
                                "1st Already in PUT position (SNAP MID order successful), nothing to do...")
                            print2file(
                                "1st Already in PUT position (SNAP MID order successful), nothing to do...")

############################################################################################################################
# Close A position before entering the LOOP for quick execution
############################################################################################################################
############################################################################################################################
# close/Exit PUT POSITION in trend reversal and still in position
ib.sleep(0.001)
if in_position == True:
    if current_time() < close_time() and current_time() >= datetime.strptime('2021-12-17 08:00:00', '%Y-%m-%d %H:%M:%S').strftime("%H:%M:%S"):  # Only time portion of datetime is evaluated
        if df['DMIPlus'].iloc[-1] > df['DMIMinus'].iloc[-1] and df['brkout'].iloc[-1] == False:
            positions = ib.positions()  # A list of positions, according to IB
            for position in positions:
                in_position = True  # True There is an open trade before start of session
                contract = Contract(conId=position.contract.conId)
                ib.qualifyContracts(contract)
                # type of contract, put('P') or call('C')
                right = position.contract.right
                if right == 'P':
                    print(
                        '***There is an Open PUT position when In_Downtrend = False, initiating close...')
                    print(contract)
                    close_trade = ib.placeOrder(
                        contract, SPX_close_snap_mid_order)  # CLOSE Call Contract

                    print("***Closing PUT in Trend Reversal Closing Order Placed")
                    print2file(
                        "***Closing PUT in Trend Reversal Closing Order Placed")
                    ib.sleep(3)  # wait for 120 secs

                    print('1st sleep')
                    if close_trade.orderStatus.status != 'Filled':
                        # cancel order type 'Snap Mid'
                        ib.cancelOrder(SPX_close_snap_mid_order)
                        ib.sleep(0.0001)
                        # Modify order to snap BUY call order
                        close_trade = ib.placeOrder(
                            contract, SPX_close_mkt_order_mod)
                        print(
                            "PUT Position Closed (MK order successful), nothing to do...")
                        print2file(
                            "PUT Position Closed (MK order successful), nothing to do...")
                        in_position = False
                        ib.disconnect()
                    else:
                        in_position = False
                        print(close_trade)
                        print(
                            "1st-PUT Position Closed (SNAP MID order successful), nothing to do...")
                        print2file(
                            "1st-PUT Position Closed (SNAP MID order successful), nothing to do...")
                        ib.disconnect()


############################################################################################################################
# close/Exit CALL POSITION in trend reversal and still in position
ib.sleep(0.001)
if in_position == True:
    if current_time() < close_time() and current_time() >= datetime.strptime('2021-12-17 08:00:00', '%Y-%m-%d %H:%M:%S').strftime("%H:%M:%S"):  # Only time portion of datetime is evaluated
        if df['DMIMinus'].iloc[-1] > df['DMIPlus'].iloc[-1] and df['brkout'].iloc[-1] == False:
            positions = ib.positions()  # A list of positions, according to IB
            for position in positions:
                in_position = True  # True There is an open trade before start of session
                contract = Contract(conId=position.contract.conId)
                ib.qualifyContracts(contract)
                # type of contract, put('P') or call('C')
                right = position.contract.right
                if right == 'C':
                    print(
                        '***There is an Open CALL position when In_Uptrend = False, initiating close...')
                    print(contract)
                    close_trade = ib.placeOrder(
                        contract, SPX_close_snap_mid_order)  # CLOSE Call Contract

                    print("***Closing CALL in Trend Reversal Closing Order Placed")
                    print2file(
                        "***Closing CALL in Trend Reversal Closing Order Placed")
                    ib.sleep(3)  # wait for 3 secs
                    print('1st sleep')
                    if close_trade.orderStatus.status != 'Filled':
                        # cancel order type 'Snap Mid'
                        ib.cancelOrder(SPX_close_snap_mid_order)
                        ib.sleep(0.0001)
                        # Modify order to snap BUY call order
                        close_trade = ib.placeOrder(
                            contract, SPX_close_mkt_order_mod)
                        print("CALL Market Closed order placed. nothing to do...")
                        print2file(
                            "CALL Market Closed order placed. nothing to do...")
                        in_position = False
                        ib.disconnect()
                    else:
                        in_position = False
                        print(close_trade)
                        print(
                            "1st-CALL Position Closed (SNAP MID order successful), nothing to do...")
                        print2file(
                            "1st-CALL Position Closed (SNAP MID order successful), nothing to do...")
                        ib.disconnect()



############################################################################################################################
# The Main loop - For Auto - Trading
def main():
    global in_position
    global open_order
    df = candle()
    print("in_position:", in_position)
    print("open_order:", open_order)
    ib.sleep(0.001)
    # Cancel open orders on re-connect which were not submitted on disconnect
    cancel_openOrders()
    # positions = ib.positions() # A list of positions, according to IB
    # position = []

    # #Check the correct value of in_position:
    # for position in positions:
    #     contract = Contract(conId = position.contract.conId)
    #     position = position.contract
    #     if position in positions:
    #         in_position = True  #True There is an open trade before start of session

    # if in_position == True and position not in ib.positions():
    #     in_position == False


############################################################################################################################
# RE-Entry - CALL
    ib.sleep(0.001)
    if in_position == False:
        if current_time() < end_order_time() and current_time() >= open_time():
            # if df['tkprofit'].iloc[-1] == False: # if max take profit for the session is reached, no more entries
            if ((df['In_Uptrend'].iloc[-1] == True and df['In_Uptrend'].iloc[-2] == False) or
                    (df['In_Uptrend'].iloc[-1] == True and df['In_Downtrend'].iloc[-1] == False)):
                if df['DMIPlus'].iloc[-1] > df['DMIPlus'].iloc[-2]:  # DMI+ uptrending
                    if df['adx'].iloc[-1] > df['adx'].iloc[-2]:  # rising ADX signify a good signal
                        if df['close'].iloc[-1] > df['open'].iloc[-1]:  # a green bar - trending up
                            # no more new trades when ADX is above adx_max_level- Max take profit for the session is reached
                            if df['maxlimit'].iloc[-1] == False or df['maxlimit2'].iloc[-1] == False:

                                trade = ib.placeOrder(
                                    call_contract(), SPX_open_snap_mid_order)
                                print("***Call Order is Placed (SNAP MID)")
                                print2file(
                                    "***Call Order is Placed (SNAP MID)")

                                # wait for, the logic for closing a trade 3 secs
                                ib.sleep(3)
                                print('1st sleep')
                                if trade.orderStatus.status != 'Filled':  # if first order type"SNAP MID" is not filled, then get ready
                                    # cancel order
                                    ib.cancelOrder(SPX_open_snap_mid_order)
                                    ib.sleep(0.0001)
                                    # Modify order, place market BUY Put order
                                    trade = ib.placeOrder(
                                        call_contract(), SPX_open_mkt_order_mod)
                                    print(trade)
                                    in_position = True
                                    print("Call Order is Placed (MKT)")
                                    print2file("Call Order is Placed (MKT)")

                                else:
                                    in_position = True
                                    print(
                                        "1st Already in CALL position (SNAP MID order successful), nothing to do...")
                                    print2file(
                                        "1st Already in CALL position (SNAP MID order successful), nothing to do...")
                            else:
                                print(
                                    "Max take profit for the session is reached - ADX level above 40, no more new trades")


# RE-Entry - PUT

            if ((df['In_Downtrend'].iloc[-1] == True and df['In_Downtrend'].iloc[-2] == False) or
                    (df['In_Downtrend'].iloc[-1] == True and df['In_Uptrend'].iloc[-1] == False)):
                if df['DMIMinus'].iloc[-1] > df['DMIMinus'].iloc[-2]:  # DMI- UPtrending
                    if df['adx'].iloc[-1] > df['adx'].iloc[-2]:  # rising ADX signify a good signal
                        if df['open'].iloc[-1] > df['close'].iloc[-1]:  # a red bar - trending up
                            trade = ib.placeOrder(
                                put_contract(), SPX_open_snap_mid_order)
                            print("***PUT Order is Placed (SNAP MID)")
                            print2file("***PUT Order is Placed (SNAP MID)")
                            ib.sleep(3)
                            # wait for, the logic for closing a trade 3 secs
                            print('1nd sleep')
                            if trade.orderStatus.status != 'Filled':  # if first order type"SNAP MID" is not filled, then get ready
                                # cancel order
                                ib.cancelOrder(SPX_open_snap_mid_order)
                                ib.sleep(0.0001)
                                # Modify order, place market BUY Put order
                                trade = ib.placeOrder(
                                    put_contract(), SPX_open_mkt_order_mod)
                                in_position = True
                                print("PUT Order is Placed (MKT)")
                                print2file("PUT Order is Placed (MKT)")

                            else:
                                in_position = True
                                print(
                                    "Already in PUT position (SNAP MID order successful), nothing to do...")
                                print2file(
                                    "Already in PUT position (SNAP MID order successful), nothing to do...")


############################################################################################################################
# Take profit at $1100/$300 target amount
    ib.sleep(0.0001)
    if in_position == True:
        ib.sleep(0.01)
        for PnL in ib.pnl(account="DU4391061"):
            unrealizedPNL = PnL.unrealizedPnL
            print("unrealized pnl: ", unrealizedPNL)

        if unrealizedPNL >= 300:  # 1100 - NDX, $300 - SPX
            positions = ib.positions()  # A list of positions, according to IB
            for position in positions:
                in_position = True  # True There is an open trade before start of session
                contract = Contract(conId=position.contract.conId)
                ib.qualifyContracts(contract)
                print('Current contract in position for $300 plus')
                print(contract)
            close_trade = ib.placeOrder(
                contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
            print('profit order placed at $300+ with SNAP MID Order ...')
            print2file('profit order placed at $300+ with SNAP MID Order ...')
            ib.sleep(3)  # wait for 3 secs
            print('1st sleep')
            ######################################################################################
            if close_trade.orderStatus.status != 'Filled':
                # cancel order type 'Snap Mid'
                ib.cancelOrder(SPX_close_snap_mid_order)
                ib.sleep(0.0001)
                # Modify order to snap BUY call order
                close_trade = ib.placeOrder(contract, SPX_close_mkt_order_mod)
                print('profit at $300+ taken with MKT Order ...')
                print2file('profit at $300+ taken with MKT Order ...')
                ib.disconnect()
                in_position = False

                # ib.disconnect()
            else:
                print('Nr 1- profit at $300+ taken with SNAP MID Order ...')
                print2file(
                    'Nr 1- profit at $300+ taken with SNAP MID Order ...')
                ib.disconnect()
                in_position = False
                # ib.disconnect()

    else:
        print('No Trades opportunities yet...')
############################################################################################################################
# Take profit at CANDLESTICK PRICE ACTION - Retracement
    ib.sleep(0.0001)
    if in_position == True:
        ib.sleep(0.1)
        for PnL in ib.pnl(account="DU4391061"):
            unrealizedPNL = PnL.unrealizedPnL
            #print("unrealized pnl: ",unrealizedPNL)

        if unrealizedPNL >= 100:
            # take profit when candle is at max range and just begin to retrace
            if (df['cndl'].iloc[-1] == 1 or df['cndl'].iloc[-1] == 2):
                positions = ib.positions()  # A list of positions, according to IB
                for position in positions:
                    in_position = True  # True There is an open trade before start of session
                    contract = Contract(conId=position.contract.conId)
                    ib.qualifyContracts(contract)
                    print('Current contract in position at cndl =1/2 and pnl >$100')
                    print(contract)
                close_trade = ib.placeOrder(
                    contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                print(
                    "Closing target at candlestick retracement >$100 $ bar cndl = 1/2. Unrealized pnl: ", unrealizedPNL)
                print2file(
                    "Closing target at candlestick retracement >$100 $ bar cndl = 1/2. Unrealized pnl: ", unrealizedPNL)

                ib.sleep(3)  # wait for 120 secs
                print('1st sleep')
                if close_trade.orderStatus.status != 'Filled':
                    # cancel order type 'Snap Mid'
                    ib.cancelOrder(SPX_close_snap_mid_order)
                    ib.sleep(0.0001)
                    # Modify order to snap BUY call order
                    close_trade = ib.placeOrder(
                        contract, SPX_close_mkt_order_mod)
                    print(
                        'profit taken at candlestick retracement >$100 $ bar cndl = 1/2. MKT Order')
                    print2file(
                        'profit taken at candlestick retracement >$100 $ bar cndl = 1/2. MKT Order')
                    ib.disconnect()
                    in_position = False
                    # ib.disconnect()
                else:
                    print(
                        'Nr 3- profit at candlestice retracement >$100 bar cndl = 1/2. taken with SNAP MID Order ...')
                    print2file(
                        'Nr 3- profit at candlestice retracement >$100 bar cndl = 1/2. taken with SNAP MID Order ...')
                    ib.disconnect()
                    in_position = False
                    # ib.disconnect()


############################################################################################################################
# Take First  profit at 7:30 - 7:34
    ib.sleep(0.0001)
    if in_position == True:
        ib.sleep(0.01)
        for PnL in ib.pnl(account="DU4391061"):
            unrealizedPNL = PnL.unrealizedPnL
            #print("unrealized pnl: ",unrealizedPNL)

        if unrealizedPNL >= 100:
            # take profit before it revereses at next bar
            if df['date'].iloc[-1].strftime("%H:%M:%S") == "07:30:00" and (df['cndl1'].iloc[-1] == 1 or df['cndl1'].iloc[-1] == 2):
                positions = ib.positions()  # A list of positions, according to IB
                for position in positions:
                    in_position = True  # True There is an open trade before start of session
                    contract = Contract(conId=position.contract.conId)
                    ib.qualifyContracts(contract)
                    print('Current contract in position at 07:34:54')
                    print(contract)
                close_trade = ib.placeOrder(
                    contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                print('SNAP MID Order placed, 07:30:00 bar cndl = 1/2')
                print2file('SNAP MID Order placed, 07:30:00 bar cndl = 1/2')

                ib.sleep(3)  # wait for 120 secs
                print('1st sleep')
                if close_trade.orderStatus.status != 'Filled':
                    # cancel order type 'Snap Mid'
                    ib.cancelOrder(SPX_close_snap_mid_order)
                    ib.sleep(0.0001)
                    # Modify order to snap BUY call order
                    close_trade = ib.placeOrder(
                        contract, SPX_close_mkt_order_mod)
                    print('profit at 07:30:00 bar cndl = 1/2. taken with MKT Order ...')
                    print2file(
                        'profit at 07:30:00 bar cndl = 1/2. taken with MKT Order ...')
                    ib.disconnect()
                    in_position = False

                    # ib.disconnect()
                else:
                    print(
                        'Nr 1- profit at 07:30:00 bar cndl = 1/2. taken with SNAP MID Order ...')
                    print2file(
                        'Nr 1- profit at 07:30:00 bar cndl = 1/2. taken with SNAP MID Order ...')
                    ib.disconnect()
                    in_position = False
                    # ib.disconnect()
############################################################################################################################
# Take profit on 2nd bar after entry
    ib.sleep(0.0001)
    if in_position == True:
        if ((df['In_Uptrend'].iloc[-2] == True or df['In_Uptrend'].iloc[-1] == True) and (df['In_Uptrend'].iloc[-3] == False)) or \
                ((df['In_Downtrend'].iloc[-2] == True or df['In_Downtrend'].iloc[-1] == True) and (df['In_Downtrend'].iloc[-3] == False)):
            # take profit when candle is at max range and just begin to retrace
            if (df['cndl2'].iloc[-1] == 1 or df['cndl2'].iloc[-1] == 2):
                ib.sleep(0.01)
                for PnL in ib.pnl(account="DU4391061"):
                    unrealizedPNL = PnL.unrealizedPnL
                    #print("unrealized pnl: ",unrealizedPNL)

                    if unrealizedPNL >= 38:
                        positions = ib.positions()  # A list of positions, according to IB
                        for position in positions:
                            in_position = True  # True There is an open trade before start of session
                            contract = Contract(conId=position.contract.conId)
                            ib.qualifyContracts(contract)

                            close_trade = ib.placeOrder(
                                contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                            print(
                                'SNAP MID Order placed, Take profit on 2nd bar after entry')
                            print2file(
                                'SNAP MID Order placed, Take profit on 2nd bar after entry')

                            ib.sleep(3)  # wait for 120 secs
                            print('1st sleep')
                            if close_trade.orderStatus.status != 'Filled':
                                # cancel order type 'Snap Mid'
                                ib.cancelOrder(SPX_close_snap_mid_order)
                                ib.sleep(0.0001)
                                # Modify order to snap BUY call order
                                close_trade = ib.placeOrder(
                                    contract, SPX_close_mkt_order_mod)
                                print(
                                    'Take profit on 2nd bar after entry. taken with MKT Order ...')
                                print2file(
                                    'Take profit on 2nd bar after entry. taken with MKT Order ...')
                                ib.disconnect()

                                in_position = False

                                # ib.disconnect()
                            else:
                                print(
                                    'Nr 1- Take profit on 2nd bar after entry. taken with SNAP MID Order ...')
                                print2file(
                                    'Nr 1- Take profit on 2nd bar after entry. taken with SNAP MID Order ...')
                                ib.disconnect()
                                in_position = False

                    # ib.disconnect()


############################################################################################################################
# Take profit at Candlestick retracement and/or bollinger band exit
    if in_position == True:
        ib.sleep(0.01)
        for PnL in ib.pnl(account="DU4391061"):
            unrealizedPNL = PnL.unrealizedPnL
            ib.sleep(0.0001)

        if unrealizedPNL >= 100:
            if ((df['cndl'].iloc[-1] == 1 and df['BB_exit'].iloc[-1] == True) or (df['cndl'].iloc[-1] == 1 and
               (df['close'].iloc[-1] > df['open'].iloc[-1] and df['close'].iloc[-2] > df['open'].iloc[-2])) or
                    (df['cndl'].iloc[-1] == 2 and df['open'].iloc[-1] > df['close'].iloc[-1] and df['open'].iloc[-2] > df['close'].iloc[-2])):  # take profit before it revereses at next bar
                positions = ib.positions()  # A list of positions, according to IB
                for position in positions:
                    in_position = True  # True There is an open trade before start of session
                    contract = Contract(conId=position.contract.conId)
                    ib.qualifyContracts(contract)
                    print('Current contract in position at 07:34:54')
                    print(contract)
                close_trade = ib.placeOrder(
                    contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                print(
                    'Take-profit at candlestic retracement + bb exit, taken with SNAP MID Order ...')
                print2file(
                    'Take-profit at candlestic retracement + bb exit, taken with SNAP MID Order ...')
                ib.sleep(3)  # wait for 120 secs
                print('1st sleep')
                if close_trade.orderStatus.status != 'Filled':
                    # cancel order type 'Snap Mid'
                    ib.cancelOrder(SPX_close_snap_mid_order)
                    ib.sleep(0.0001)
                    # Modify order to snap BUY call order
                    close_trade = ib.placeOrder(
                        contract, SPX_close_mkt_order_mod)
                    print(
                        'profit TAKEN at candlestic price retracement + bb exit taken with MKT Order ...')
                    print2file(
                        'profit TAKEN at candlestic price retracement + bb exit taken with MKT Order ...')
                    ib.disconnect()
                    in_position = False
                    # ib.disconnect()
                else:
                    print(
                        'Nr 1- profit at candlestic price retracement + bb exit taken with SNAP MID Order ...')
                    print2file(
                        'Nr 1- profit at candlestic price retracement + bb exit taken with SNAP MID Order ...')
                    ib.disconnect()
                    in_position = False
                    # ib.disconnect()

############################################################################################################################
# Take profit at Candlestick retracement and/or prev bollinger band exit 2***************************************************
    if in_position == True:
        ib.sleep(0.01)
        for PnL in ib.pnl(account="DU4391061"):
            unrealizedPNL = PnL.unrealizedPnL
            ib.sleep(0.0001)

            if unrealizedPNL >= 5:
                if (df['cndl'].iloc[-2] == 1 and df['BB_exit'].iloc[-2] == True and df['close'].iloc[-2] > df['open'].iloc[-2] and
                   df['DMIPlus'].iloc[-1] > df['DMIMinus'].iloc[-1] and df['DMIPlus'].iloc[-1] > df['DMIPlus'].iloc[-2]) or \
                   (df['cndl'].iloc[-2] == 2 and df['BB_exit'].iloc[-2] == True and df['open'].iloc[-2] > df['close'].iloc[-2] and
                   df['DMIMinus'].iloc[-1] < df['DMIPlus'].iloc[-1] and df['DMIMinus'].iloc[-1] < df['DMIMinus'].iloc[-2]):
                    # take profit before it revereses at next bar
                    positions = ib.positions()  # A list of positions, according to IB
                    for position in positions:
                        in_position = True  # True There is an open trade before start of session
                        contract = Contract(conId=position.contract.conId)
                        ib.qualifyContracts(contract)
                    close_trade = ib.placeOrder(
                        contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                    print(
                        'Take-profit at desc candlestic retracement + bb exit, taken with SNAP MID Order ...')
                    print2file(
                        'Take-profit at desc candlestic retracement + bb exit, taken with SNAP MID Order ...')
                    ib.sleep(3)  # wait for 120 secs
                    print('1st sleep')
                    if close_trade.orderStatus.status != 'Filled':
                        # cancel order type 'Snap Mid'
                        ib.cancelOrder(SPX_close_snap_mid_order)
                        ib.sleep(0.0001)
                        # Modify order to snap BUY call order
                        close_trade = ib.placeOrder(
                            contract, SPX_close_mkt_order_mod)
                        print(
                            'profit TAKEN at desc candlestic price retracement + bb exit taken with MKT Order ...')
                        print2file(
                            'profit TAKEN at desc candlestic price retracement + bb exit taken with MKT Order ...')
                        ib.disconnect()
                        in_position = False

                        # ib.disconnect()
                    else:
                        print(
                            'Nr 1- profit at desc candlestic price retracement + bb exit taken with SNAP MID Order ...')
                        print2file(
                            'Nr 1- profit at desc candlestic price retracement + bb exit taken with SNAP MID Order ...')
                        ib.disconnect()
                        in_position = False
                        # ib.disconnect()

############################################################################################################################
# Take profit at above and beyond bb exit, next bar
    if in_position == True:
        ib.sleep(0.3)
        for PnL in ib.pnl(account="DU4391061"):
            unrealizedPNL = PnL.unrealizedPnL
            #print("unrealized pnl: ",unrealizedPNL)
        if unrealizedPNL >= 100:
            if abs(df['open'].iloc[-2]-df['close'].iloc[-2]) > df['atr'].iloc[-1] and\
                    df['BB_exit'].iloc[-2] == True and df['BB_exit'].iloc[-1] == True and (df['cndl2'].iloc[-1] == 1 or df['cndl2'].iloc[-1] == 2):  # body of previous candle is > atr and above bb, exit at next candle
                positions = ib.positions()  # A list of positions, according to IB
                for position in positions:
                    in_position = True  # True There is an open trade before start of session
                    contract = Contract(conId=position.contract.conId)
                    ib.qualifyContracts(contract)
                    print('Current contract above and beyond bb exit')
                    print(contract)
                close_trade = ib.placeOrder(
                    contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                print(
                    'Take profit SNAP MID order placed with previous and current bb exit and pnl>$100...')
                print2file(
                    'Take profit SNAP MID order placed with previous and current bb exit and pnl>$100...')
                ib.sleep(3)  # wait for 120 secs
                print('1st sleep')
                if close_trade.orderStatus.status != 'Filled':
                    # cancel order type 'Snap Mid'
                    ib.cancelOrder(SPX_close_snap_mid_order)
                    ib.sleep(0.0001)
                    # Modify order to snap BUY call order
                    close_trade = ib.placeOrder(
                        contract, SPX_close_mkt_order_mod)
                    print(
                        'profit order placed with previous and current bb exit and pnl>$100 - MKT Order taken ...')
                    print2file(
                        'profit order placed with previous and current bb exit and pnl>$100 - MKT Order taken ...')
                    ib.disconnect()
                    in_position = False

                else:
                    print(
                        'Nr 3- profit order placed with previous and current bb exit and pnl>$100 - SNAP MID ...')
                    print2file(
                        'Nr 3- profit order placed with previous and current bb exit and pnl>$100 - SNAP MID ...')
                    ib.disconnect()
                    in_position = False
                    # ib.disconnect()
############################################################################################################################
# Take profit at above and beyond bb exit using metric on the bar
    if in_position == True:
        ib.sleep(0.01)
        for PnL in ib.pnl(account="DU4391061"):
            unrealizedPNL = PnL.unrealizedPnL
            #print("unrealized pnl: ",unrealizedPNL)
        if unrealizedPNL >= 100:
            if ((df['high'].iloc[-1]-df['upper_band'].iloc[-1])/df['upper_band'].iloc[-1])*100 > 0.1 or\
                    ((df['lower_band'].iloc[-1]-df['low'].iloc[-1])/df['lower_band'].iloc[-1])*100 > 0.1:  # body of previous candle is > atr and above bb, exit at next candle

                positions = ib.positions()  # A list of positions, according to IB
                for position in positions:
                    in_position = True  # True There is an open trade before start of session
                    contract = Contract(conId=position.contract.conId)
                    ib.qualifyContracts(contract)
                    print('Current contract at/on beyond bb exit')
                    print(contract)
                close_trade = ib.placeOrder(
                    contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                print(
                    'Take profit beyond bb exit on CURRENT BAR using metric with SNAP MID Order placed ...')
                print2file(
                    'Take profit beyond bb exit on CURRENT BAR using metric with SNAP MID Order placed ...')
                ib.sleep(3)  # wait for 120 secs
                print('1st sleep')
                if close_trade.orderStatus.status != 'Filled':
                    # cancel order type 'Snap Mid'
                    ib.cancelOrder(SPX_close_snap_mid_order)
                    ib.sleep(0.0001)
                    # Modify order to snap BUY call order
                    close_trade = ib.placeOrder(
                        contract, SPX_close_mkt_order_mod)
                    print(
                        'Take profit beyond bb exit on CURRENT BAR using metric with MKT Order ...')
                    print2file(
                        'Take profit beyond bb exit on CURRENT BAR using metric with MKT Order ...')
                    ib.disconnect()
                    in_position = False
                else:
                    print(
                        'Nr 1- Take profit beyond bb exit on CURRENT BAR using metric with SNAP MID Order ...')
                    print2file(
                        'Nr 1- Take profit beyond bb exit on CURRENT BAR using metric with SNAP MID Order ...')
                    ib.disconnect()
                    in_position = False
                    # ib.disconnect()
                    #
############################################################################################################################
# Take profit after 3rd candlestick >$100
    if in_position == True:
        ib.sleep(0.01)
        for PnL in ib.pnl(account="DU4391061"):
            unrealizedPNL = PnL.unrealizedPnL
            #print("unrealized pnl: ",unrealizedPNL)
        if unrealizedPNL >= 100:
            if (df['cndl2'].iloc[-1] == 1 or df['cndl2'].iloc[-1] == 2) and \
                ((df['close'].iloc[-1] > df['open'].iloc[-1] and df['close'].iloc[-2] > df['open'].iloc[-2] and df['close'].iloc[-3] > df['open'].iloc[-3]) or
                 (df['open'].iloc[-1] > df['close'].iloc[-1] and df['open'].iloc[-2] > df['close'].iloc[-2] and df['open'].iloc[-3] > df['close'].iloc[-3])):
                positions = ib.positions()  # A list of positions, according to IB
                for position in positions:
                    in_position = True  # True There is an open trade before start of session
                    contract = Contract(conId=position.contract.conId)
                    ib.qualifyContracts(contract)
                close_trade = ib.placeOrder(
                    contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                print('Take profit after 3rd candlestick >$100 - order placed SNAP MID ')
                print2file(
                    'Take profit after 3rd candlestick >$100 - order placed SNAP MID ')

                ib.sleep(3)  # wait for 120 secs
                print('1st sleep')
                if close_trade.orderStatus.status != 'Filled':
                    # cancel order type 'Snap Mid'
                    ib.cancelOrder(SPX_close_snap_mid_order)
                    ib.sleep(0.0001)
                    # Modify order to snap BUY call order
                    close_trade = ib.placeOrder(
                        contract, SPX_close_mkt_order_mod)
                    print('Take profit 3rd candlestick >$100 with MKT Order ...')
                    print2file(
                        'Take profit 3rd candlestick >$100 with MKT Order ...')
                    ib.disconnect()
                    in_position = False

                else:
                    print('Nr 1- profit 3rd candlestick >$100 with SNAP MID Order ...')
                    print2file(
                        'Nr 1- profit 3rd candlestick >$100 with SNAP MID Order ...')
                    ib.disconnect()
                    in_position = False
                    # ib.disconnect()
############################################################################################################################
# Take profit at ATR below 5 >$100
    if in_position == True:
        ib.sleep(0.01)
        for PnL in ib.pnl(account="DU4391061"):
            unrealizedPNL = PnL.unrealizedPnL
            #print("unrealized pnl: ",unrealizedPNL)
        if unrealizedPNL >= 100:
            if (df['cndl2'].iloc[-1] == 1 or df['cndl2'].iloc[-1] == 2) and \
                    (df['atr'].iloc[-2] < 5 and df['atr'].iloc[-3] < 5):
                positions = ib.positions()  # A list of positions, according to IB
                for position in positions:
                    in_position = True  # True There is an open trade before start of session
                    contract = Contract(conId=position.contract.conId)
                    ib.qualifyContracts(contract)
                close_trade = ib.placeOrder(
                    contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                print('Take profit atr less than 5 and >$100 - order placed SNAP MID ')
                print2file(
                    'Take profit atr less than 5 and >$100 - order placed SNAP MID ')

                ib.sleep(3)  # wait for 120 secs
                print('1st sleep')
                if close_trade.orderStatus.status != 'Filled':
                    # cancel order type 'Snap Mid'
                    ib.cancelOrder(SPX_close_snap_mid_order)
                    ib.sleep(0.0001)
                    # Modify order to snap BUY call order
                    close_trade = ib.placeOrder(
                        contract, SPX_close_mkt_order_mod)
                    print('Take profit 3rd candlestick >$100 with MKT Order ...')
                    print2file(
                        'Take profit 3rd candlestick >$100 with MKT Order ...')
                    ib.disconnect()
                    in_position = False

                else:
                    print('Nr 1- profit 3rd candlestick >$100 with SNAP MID Order ...')
                    print2file(
                        'Nr 1- profit 3rd candlestick >$100 with SNAP MID Order ...')
                    ib.disconnect()
                    in_position = False
                    # ib.disconnect()
############################################################################################################################
# Take profit at ATR below 4 >$58 AND adx below threshold - 20
    if in_position == True:
        ib.sleep(0.01)
        for PnL in ib.pnl(account="DU4391061"):
            unrealizedPNL = PnL.unrealizedPnL
            #print("unrealized pnl: ",unrealizedPNL)
        if unrealizedPNL >= 58:
            if (df['cndl2'].iloc[-1] == 1 or df['cndl2'].iloc[-1] == 2) and \
                    (df['atr'].iloc[-2] < 2 and df['atr'].iloc[-3] < 2):
                positions = ib.positions()  # A list of positions, according to IB
                for position in positions:
                    in_position = True  # True There is an open trade before start of session
                    contract = Contract(conId=position.contract.conId)
                    ib.qualifyContracts(contract)
                close_trade = ib.placeOrder(
                    contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                print('Take profit atr < 2 pnl >$58 - order placed SNAP MID ')
                print2file(
                    'Take profit atr < 2 pnl >$58 - order placed SNAP MID ')

                ib.sleep(3)  # wait for 120 secs
                print('1st sleep')
                if close_trade.orderStatus.status != 'Filled':
                    # cancel order type 'Snap Mid'
                    ib.cancelOrder(SPX_close_snap_mid_order)
                    ib.sleep(0.0001)
                    # Modify order to snap BUY call order
                    close_trade = ib.placeOrder(
                        contract, SPX_close_mkt_order_mod)
                    print('Take profit atr < 2 pnl >$58  with MKT Order ...')
                    print2file(
                        'Take profit atr < 4 pnl >$58 with MKT Order ...')
                    ib.disconnect()
                    in_position = False

                else:
                    print('Nr 1- Take profit atr < 2 pnl >$58  with SNAP MID Order ...')
                    print2file(
                        'Nr 1- Take profit atr < 2 pnl >$58 with SNAP MID Order ...')
                    ib.disconnect()
                    in_position = False
                    # ib.disconnect()
############################################################################################################################
# #Limit Loss at -$1000
    if in_position == True:
        ib.sleep(0.01)
        for PnL in ib.pnl(account="DU4391061"):
            unrealizedPNL = PnL.unrealizedPnL
            #print("unrealized pnl: ",unrealizedPNL)
        if unrealizedPNL <= -1000:
            if (df['DMIMinus'].iloc[-1] < threshold or df['DMIPlus'].iloc[-1] < threshold) and \
                    (df['DMIPlus'].iloc[-1] < df['DMIPlus'].iloc[-2] or df['DMIMinus'].iloc[-1] < df['DMIMinus'].iloc[-2]):
                positions = ib.positions()  # A list of positions, according to IB
                for position in positions:
                    in_position = True  # True There is an open trade before start of session
                    contract = Contract(conId=position.contract.conId)
                    ib.qualifyContracts(contract)
                close_trade = ib.placeOrder(
                    contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                print('Max stoploss reached >-$1000 - order placed SNAP MID ')
                print2file(
                    'Max stoploss reached >-$1000  - order placed SNAP MID ')

                ib.sleep(3)  # wait for 120 secs
                print('1st sleep')
                if close_trade.orderStatus.status != 'Filled':
                    # cancel order type 'Snap Mid'
                    ib.cancelOrder(SPX_close_snap_mid_order)
                    ib.sleep(0.0001)
                    # Modify order to snap BUY call order
                    close_trade = ib.placeOrder(
                        contract, SPX_close_mkt_order_mod)
                    print('Max stoploss reached >-$1000 with MKT Order ...')
                    print2file(
                        'Max stoploss reached >-$1000  with MKT Order ...')
                    ib.disconnect()
                    in_position = False
                else:
                    print('Nr 1- Max stoploss reached >-$1000  with SNAP MID Order ...')
                    print2file(
                        'Nr 1- Max stoploss reached >-$1000  with SNAP MID Order ...')
                    ib.disconnect()
                    in_position = False
                    # ib.disconnect()
############################################################################################################################
# Take PROFIT AT DECLINING TREND (tkprofit) >$100
    if in_position == True:
        ib.sleep(0.01)
        for PnL in ib.pnl(account="DU4391061"):
            unrealizedPNL = PnL.unrealizedPnL
            #print("unrealized pnl: ",unrealizedPNL)
        if unrealizedPNL >= 100:
            if (df['cndl2'].iloc[-1] == 1 or df['cndl2'].iloc[-1] == 2) and\
                    df['tkprofit'].iloc[-2] == True:  # take profit after every $100 and higher at declining trend (df['tkprofit'])
                positions = ib.positions()  # A list of positions, according to IB
                for position in positions:
                    in_position = True  # True There is an open trade before start of session
                    contract = Contract(conId=position.contract.conId)
                    ib.qualifyContracts(contract)
                close_trade = ib.placeOrder(
                    contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                print(
                    'Take profit at  declining trend (tkprofit) >$100 - order placed SNAP MID ')
                print2file(
                    'Take profit at  declining trend (tkprofit) >$100 - order placed SNAP MID  ')

                ib.sleep(3)  # wait for 120 secs
                print('1st sleep')
                if close_trade.orderStatus.status != 'Filled':
                    # cancel order type 'Snap Mid'
                    ib.cancelOrder(SPX_close_snap_mid_order)
                    ib.sleep(0.0001)
                    # Modify order to snap BUY call order
                    close_trade = ib.placeOrder(
                        contract, SPX_close_mkt_order_mod)
                    print(
                        'Take profit at  declining trend (tkprofit) >$100 with MKT Order ...')
                    print2file(
                        'Take profit AT  declining trend (tkprofit) >$100 with MKT Order ...')
                    ib.disconnect()
                    in_position = False
                else:
                    print(
                        'Nr 1- profit at  declining trend (tkprofit) >$100 with SNAP MID Order ...')
                    print2file(
                        'Nr 1- profit at  declining trend (tkprofit) >$100 with SNAP MID Order ...')
                    ib.disconnect()
                    in_position = False
############################################################################################################################
# First Bollinger Band Exit - 4 bars trending and now exiting BB (high-risk of reversal)
    if in_position == True:
        if df['D'].iloc[-2] == True:  # PREVIOUS BB EXIT
            ib.sleep(0.01)
            for PnL in ib.pnl(account="DU4391061"):
                unrealizedPNL = PnL.unrealizedPnL
                print("unrealized pnl: ", unrealizedPNL)
                if unrealizedPNL >= 5:  # Simulate value. If its a profit at the time of exiting bb, after a few previous trending bars, then exit, high probability of reversal
                    positions = ib.positions()  # A list of positions, according to IB
                    for position in positions:
                        in_position = True  # True There is an open trade before start of session
                        contract = Contract(conId=position.contract.conId)
                        ib.qualifyContracts(contract)
                        # type of contract, put('P') or call('C')
                        right = position.contract.right
                        # Exiting PUT
                        if right == 'P':  # if its a PUT
                            # DMI- up downtrending
                            if (df['DMIMinus'].iloc[-1] < df['DMIMinus'].iloc[-2]) or (df['close'].iloc[-1] > df['open'].iloc[-1]):
                                # and df['close'].iloc[-1]>df['open'].iloc[-1] #a green bar - trending up after exiting bb

                                close_trade = ib.placeOrder(
                                    contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                                print(
                                    'BB Order close Placed high risk of reversal ')
                                print2file(
                                    'BB Order close Placed high risk of reversal ')

                                ib.sleep(3)  # wait for 120 secs
                                print('1st sleep')
                                if close_trade.orderStatus.status != 'Filled':
                                    # cancel order type 'Snap Mid'
                                    ib.cancelOrder(SPX_close_snap_mid_order)
                                    ib.sleep(0.0001)
                                    # Modify order to snap BUY call order
                                    close_trade = ib.placeOrder(
                                        contract, SPX_close_mkt_order_mod)
                                    print(close_trade)
                                    in_position = False
                                    print(
                                        "MKT order filled...BB TARGET Position Closed...")
                                    print2file(
                                        "MKT order filled...BB TARGET Position Closed...")
                                    ib.disconnect()
                                    in_position = False
                                    # ib.disconnect()
                                else:

                                    print(
                                        "1st-SNAP MID  high-risk order filled-BB TARGET Closed...")
                                    print2file(
                                        "1st-SNAP MID  high-risk order filled-BB TARGET Closed...")
                                    ib.disconnect()
                                    in_position = False
                                    # ib.disconnect()

                        # Exiting CALL
                        elif right == 'C':  # if its a Call
                            # DMI- up downtrending
                            if (df['DMIPlus'].iloc[-1] < df['DMIPlus'].iloc[-2]) or (df['open'].iloc[-1] > df['close'].iloc[-1]):
                                # if and df['open'].iloc[-1]>df['close'].iloc[-1]  #a red bar - trending DOWN after exiting bb
                                close_trade = ib.placeOrder(
                                    contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                                print(
                                    'BB CALL Order Placed high risk. Position is green')
                                print2file(
                                    'BB CALL Order Placed high risk. Position is green')
                                ib.sleep(3)  # wait for 120 secs
                                print('1st sleep')
                                if close_trade.orderStatus.status != 'Filled':
                                    # cancel order type 'Snap Mid'
                                    ib.cancelOrder(SPX_close_snap_mid_order)
                                    ib.sleep(0.0001)
                                    # Modify order to snap BUY call order
                                    close_trade = ib.placeOrder(
                                        contract, SPX_close_mkt_order_mod)
                                    print(close_trade)
                                    in_position = False
                                    print(
                                        "MKT CALL order filled...BB TARGET Position Closed...")
                                    print2file(
                                        "MKT CALL order filled...BB TARGET Position Closed...")
                                    ib.disconnect()
                                    in_position = False
                                    # ib.disconnect()
                                else:
                                    in_position = False
                                    print(
                                        "1st-SNAP MID CALL order high-risk order filled-BB TARGET Closed...")
                                    print2file(
                                        "1stth-SNAP MID CALL order high-risk order filled-BB TARGET Closed...")
                                    ib.disconnect()
                                    in_position = False
                                    # ib.disconnect()
############################################################################################################################
# close/Exit PUT POSITION in trend reversal and still in position
    ib.sleep(0.001)
    if in_position == True:
        if current_time() < close_time() and current_time() >= datetime.strptime('2021-12-17 08:00:00', '%Y-%m-%d %H:%M:%S').strftime("%H:%M:%S"):  # Only time portion of datetime is evaluated
            if df['DMIPlus'].iloc[-1] > df['DMIMinus'].iloc[-1] and df['brkout'].iloc[-1] == False:
                positions = ib.positions()  # A list of positions, according to IB
                for position in positions:
                    in_position = True  # True There is an open trade before start of session
                    contract = Contract(conId=position.contract.conId)
                    ib.qualifyContracts(contract)
                    # type of contract, put('P') or call('C')
                    right = position.contract.right
                    if right == 'P':
                        print(
                            '***There is an Open PUT position when In_Downtrend = False, initiating close...')
                        print(contract)
                        close_trade = ib.placeOrder(
                            contract, SPX_close_snap_mid_order)  # CLOSE Call Contract
                        print("***Closing PUT in Trend Reversal Closing Order Placed")
                        print2file(
                            "***Closing PUT in Trend Reversal Closing Order Placed")

                        ib.sleep(3)  # wait for 120 secs

                        print('1st sleep')
                        if close_trade.orderStatus.status != 'Filled':
                            # cancel order type 'Snap Mid'
                            ib.cancelOrder(SPX_close_snap_mid_order)
                            ib.sleep(0.0001)
                            # Modify order to snap BUY call order
                            close_trade = ib.placeOrder(
                                contract, SPX_close_mkt_order_mod)
                            print(
                                "PUT Reversal Position Closed (MKT order successful), nothing to do...")
                            print2file(
                                "PUT Reversal Position Closed (MKT order successful), nothing to do...")
                            ib.disconnect()
                            in_position = False

                        else:
                            print(
                                "6th-PUT reversal Position Closed (MKT order successful), nothing to do...")
                            print2file(
                                "6th-PUT reversal Position Closed (MKT order successful), nothing to do...")
                            ib.disconnect()
                            in_position = False

############################################################################################################################
# close/Exit CALL POSITION in trend reversal and still in position
    ib.sleep(0.001)
    if in_position == True:
        if current_time() < close_time() and current_time() >= datetime.strptime('2021-12-17 08:00:00', '%Y-%m-%d %H:%M:%S').strftime("%H:%M:%S"):  # Only time portion of datetime is evaluated
            if df['DMIMinus'].iloc[-1] > df['DMIPlus'].iloc[-1] and df['brkout'].iloc[-1] == False:
                positions = ib.positions()  # A list of positions, according to IB
                for position in positions:
                    in_position = True  # True There is an open trade before start of session
                    contract = Contract(conId=position.contract.conId)
                    ib.qualifyContracts(contract)
                    # type of contract, put('P') or call('C')
                    right = position.contract.right
                    if right == 'C':
                        print(
                            '***There is an Open CALL position when In_Uptrend = False, initiating close...')
                        print(contract)
                        close_trade = ib.placeOrder(
                            contract, SPX_close_snap_mid_order)  # CLOSE Call Contract
                        print(
                            "***Closing CALL in Trend Reversal Closing Order Placed")
                        print(
                            "***Closing CALL in Trend Reversal Closing Order Placed")
                        ib.sleep(3)  # wait for 120 secs

                        print('1st sleep')
                        if close_trade.orderStatus.status != 'Filled':
                            # cancel order type 'Snap Mid'
                            ib.cancelOrder(SPX_close_snap_mid_order)
                            ib.sleep(0.0001)
                            # Modify order to snap BUY call order
                            close_trade = ib.placeOrder(
                                contract, SPX_close_mkt_order_mod)
                            print(
                                "CALL Market Closed order placed. nothing to do...")
                            print2file(
                                "CALL Market Closed order placed. nothing to do...")
                            ib.disconnect()
                            in_position = False

                        else:
                            in_position = False
                            print(
                                "1st-CALL Position Closed (SNAP MID order successful), nothing to do...")
                            print2file(
                                "1st-CALL Position Closed (SNAP MID order successful), nothing to do...")
                            ib.disconnect()
                            in_position = False
############################################################################################################################
# GAP UP TRADE (same direction) - CALL
    ib.sleep(0.001)
    if in_position == False:
        if df['DMIPlus'].iloc[-1] > df['DMIMinus'].iloc[-1] and df['adx'].iloc[-1] > df['adx'].iloc[-2] and df['brkout'].iloc[-1] == True:
            # Only time portion of datetime is evaluated
            if current_time() > datetime.strptime('2021-12-17 07:30:00', '%Y-%m-%d %H:%M:%S').strftime("%H:%M:%S"):
                if current_time() < datetime.strptime('2021-12-17 07:35:00', '%Y-%m-%d %H:%M:%S').strftime("%H:%M:%S"):
                    # Opening greater than prev bar's high or yesterday lastbar high
                    if df['open'].iloc[-1] > df['high'].iloc[-2]:
                        # rising ADX signify a good signal
                        if df['adx'].iloc[-1] > df['adx'].iloc[-2]:
                            # a green bar - trending up
                            if df['close'].iloc[-1] > df['open'].iloc[-1]:
                                trade = ib.placeOrder(
                                    call_contract(), SPX_open_snap_mid_order)
                                # registering entry price, used for backtesting
                                bp = df['close'].iloc[-1]
                                print(
                                    "Day Open Gap Up Call trade Placed (SNAP MID)")
                                print2file(
                                    "Day Open Gap Up Call trade Placed (SNAP MID)")
                                ib.sleep(3)  # wait for 3 secs
                                print('1st sleep')
                                if trade.orderStatus.status != 'Filled':  # if first order type"SNAP MID" is not filled, then get ready
                                    # cancel order
                                    ib.cancelOrder(SPX_open_snap_mid_order)
                                    ib.sleep(0.001)
                                    # Modify order, place market BUY Put order
                                    trade = ib.placeOrder(
                                        call_contract(), SPX_open_mkt_order_mod)
                                    in_position = True
                                    print(
                                        "Day Open Gap Up CALL trade placed (MKT)")
                                    print2file(
                                        "Day Open Gap Up CALL trade placed (MKT)")

                                else:
                                    in_position = True
                                    print(
                                        "1st-Already in Day Open Gap Up  CALL trade  (SNAP MID order successful), nothing to do...")
                                    print2file(
                                        "1st-Already in Day Open Gap Up  CALL trade  (SNAP MID order successful), nothing to do...")

############################################################################################################################
# GAP DOWN TRADE (same direction) - PUT
    ib.sleep(0.001)
    if in_position == False:
        if df['DMIMinus'].iloc[-1] > df['DMIPlus'].iloc[-1] and df['adx'].iloc[-1] > df['adx'].iloc[-2] and df['brkout'].iloc[-1] == True:
            # Only time portion of datetime is evaluated
            if current_time() > datetime.strptime('2021-12-17 07:30:00', '%Y-%m-%d %H:%M:%S').strftime("%H:%M:%S"):
                if current_time() < datetime.strptime('2021-12-17 07:35:00', '%Y-%m-%d %H:%M:%S').strftime("%H:%M:%S"):
                    # Opening less than prev bar's LOW or prev day's last bar low
                    if df['open'].iloc[-1] < df['low'].iloc[-2]:
                        # rising ADX signify a good signal
                        if df['adx'].iloc[-1] > df['adx'].iloc[-2]:
                            # a red bar - trending DOWN
                            if df['open'].iloc[-1] > df['close'].iloc[-1]:
                                trade = ib.placeOrder(
                                    put_contract(), SPX_open_snap_mid_order)
                                # registering entry price, used for backtesting
                                bp = df['close'].iloc[-1]
                                print("Opening Gap Up PUT trade Placed (SNAP MID)")
                                print2file(
                                    "Opening Gap Up PUT trade Placed (SNAP MID)")
                                ib.sleep(3)  # wait for 3 secs
                                print('1st sleep')
                                ######################################################################################
                                if trade.orderStatus.status != 'Filled':  # if first order type"SNAP MID" is not filled, then get ready
                                    # cancel order
                                    ib.cancelOrder(SPX_open_snap_mid_order)
                                    ib.sleep(0.001)
                                    # Modify order, place market BUY Put order
                                    trade = ib.placeOrder(
                                        put_contract(), SPX_open_mkt_order_mod)
                                    print("Opening Gap Up Put trade placed (MKT)")
                                    print2file(
                                        "Opening Gap Up Put trade placed (MKT)")
                                    in_position = True
                                else:
                                    print(
                                        "1st-Already in Opening Gap Up Put trade  (SNAP MID order successful), nothing to do...")
                                    print2file(
                                        "1st-Already in Opening Gap Up Put trade  (SNAP MID order successful), nothing to do...")
                                    in_position = True
############################################################################################################################
# TAKE PROFIT - CALL (Exiting CALL)
    ib.sleep(0.001)
    if in_position == True:
        if current_time() < close_time():
            for PnL in ib.pnl(account="DU4391061"):
                unrealizedPNL = PnL.unrealizedPnL
                print("unrealized pnl: ", unrealizedPNL)
                if unrealizedPNL >= 50:
                    if df['In_Uptrend'].iloc[-1] == True:
                        if df['tkprofit'].iloc[-1] == True or \
                            (df['In_Uptrend'].iloc[-1] == True and df['brkout'].iloc[-1] == True and
                                current_time() > datetime.strptime('2021-12-17 07:35:00', '%Y-%m-%d %H:%M:%S').strftime("%H:%M:%S")):  # EARLY TAKE PROFIT  in the day or at opening

                            # current DMI+ down downtrending
                            if df['DMIPlus'].iloc[-1] < df['DMIPlus'].iloc[-2]:
                                positions = ib.positions()  # A list of positions, according to IB
                                for position in positions:
                                    in_position = True  # True There is an open trade before start of session
                                    contract = Contract(
                                        conId=position.contract.conId)
                                    ib.qualifyContracts(contract)
                                    # type of contract, put('P') or call('C')
                                    right = position.contract.right
                                    # Exiting CALL
                                    if right == 'C':  # it a CALL
                                        close_trade = ib.placeOrder(
                                            contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                                        print(
                                            'Early Call(brkout) Take-Profit Reached- Closing Call Order Placed ...')
                                        print2file(
                                            'Early Call(brkout) Take-Profit Reached- Closing Call Order Placed ...')

                                        ib.sleep(3)  # wait for 120 secs
                                        print('1st sleep')
                                        if close_trade.orderStatus.status != 'Filled':
                                            # cancel order type 'Snap Mid'
                                            ib.cancelOrder(
                                                SPX_close_snap_mid_order)
                                            ib.sleep(0.0001)
                                            # Modify order to snap BUY call order
                                            close_trade = ib.placeOrder(
                                                contract, SPX_close_mkt_order_mod)
                                            print(close_trade)
                                            print(
                                                "MKT Call order filled...Early Take-Profit Reached. Position Closed...")
                                            print2file(
                                                "MKT Call order filled...Early Take-Profit Reached. Position Closed...")
                                            ib.disconnect()
                                            in_position = False
                                        else:
                                            in_position = False
                                            print(
                                                "1st-SNAP MID Call Early Take-Profit Reached - order filled...")
                                            print2file(
                                                "1st-SNAP MID Call Early Take-Profit Reached - order filled...")
                                            ib.disconnect()
                                            in_position = False
############################################################################################################################
# TAKE PROFIT - PUT (Exiting PUT)
    ib.sleep(0.001)
    if in_position == True:
        if current_time() < close_time():
            for PnL in ib.pnl(account="DU4391061"):
                unrealizedPNL = PnL.unrealizedPnL
                print("unrealized pnl: ", unrealizedPNL)
                if unrealizedPNL >= 50:
                    if ((df['In_Downtrend'].iloc[-1] == True) or (df['DMIMinus'].iloc[-1] > df['DMIPlus'].iloc[-1]) and df['adx'].iloc[-1] < adx_threshold):
                        if df['tkprofit'].iloc[-1] == True or \
                            (df['In_Downtrend'].iloc[-1] == True and df['brkout'].iloc[-1] == True and
                             current_time() > datetime.strptime('2021-12-17 07:35:00', '%Y-%m-%d %H:%M:%S').strftime("%H:%M:%S")):  # EARLY TAKE PROFIT
                            # current DMI+ down downtrending
                            if df['DMIMinus'].iloc[-1] < df['DMIMinus'].iloc[-2]:
                                positions = ib.positions()  # A list of positions, according to IB
                                for position in positions:
                                    in_position = True  # True There is an open trade before start of session
                                    contract = Contract(
                                        conId=position.contract.conId)
                                    ib.qualifyContracts(contract)
                                    # type of contract, put('P') or PUT('C')
                                    right = position.contract.right
                                    # Exiting PUT
                                    if right == 'P':  # it a PUT
                                        close_trade = ib.placeOrder(
                                            contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                                        print(
                                            'Early Take-Profit Reached - Closing PUT Order Placed ...')
                                        print2file(
                                            'Early Take-Profit Reached - Closing PUT Order Placed ...')

                                        ib.sleep(3)  # wait for 120 secs
                                        print('1st sleep')
                                        if close_trade.orderStatus.status != 'Filled':
                                            # cancel order type 'Snap Mid'
                                            ib.cancelOrder(
                                                SPX_close_snap_mid_order)
                                            ib.sleep(0.0001)
                                            # Modify order to snap BUY PUT order
                                            close_trade = ib.placeOrder(
                                                contract, SPX_close_mkt_order_mod)
                                            in_position = False
                                            print(
                                                "MKT PUT order filled...Early Take-Profit Reached. Position Closed...")
                                            print2file(
                                                "MKT PUT order filled...Early Take-Profit Reached. Position Closed...")
                                            ib.disconnect()
                                            in_position = False

                                        else:
                                            in_position = False
                                            print(
                                                "1st-SNAP MID Early Take-Profit Reached - order filled...")
                                            print2file(
                                                "1st-SNAP MID Early Take-Profit Reached - order filled...")
                                            ib.disconnect()
                                            in_position = False
############################################################################################################################
# FALSE TREND SIGNAL CORRECTION - CLOSING OPEN TRADE******************************
    ib.sleep(0.001)
    if in_position == True:
        if current_time() < close_time():
            # downtrend curent and previous false
            if (df['In_Downtrend'].iloc[-1] == False and df['In_Downtrend'].iloc[-2] == False):
                # up trend curent and previous false
                if (df['In_Uptrend'].iloc[-1] == False and df['In_Uptrend'].iloc[-2] == False):
                    if (df['gap'].iloc[-1] == 0 and df['gap'].iloc[-2] == 0 and df['gap'].iloc[-3] == 0 and df['brkout'].iloc[-1] == False):  # if its a gap up
                        positions = ib.positions()  # A list of positions, according to IB
                        for position in positions:
                            in_position = True  # True There is an open trade
                            contract = Contract(conId=position.contract.conId)
                            ib.qualifyContracts(contract)
                            # type of contract, put('P') or PUT('C')
                            right = position.contract.right
                            close_trade = ib.placeOrder(
                                contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                            print(
                                'FALSE TREND SIGNAL - Closing TRADE  Order Placed ...')
                            print2file(
                                'FALSE TREND SIGNAL - Closing TRADE  Order Placed ...')
                            ib.sleep(3)  # wait for 120 secs
                            print('1st sleep')
                            if close_trade.orderStatus.status != 'Filled':
                                # cancel order type 'Snap Mid'
                                ib.cancelOrder(SPX_close_snap_mid_order)
                                ib.sleep(0.0001)
                                # Modify order to snap BUY PUT order
                                close_trade = ib.placeOrder(
                                    contract, SPX_close_mkt_order_mod)
                                in_position = False
                                print(
                                    "MKT order filled...FALSE TREND SIGNAL - Closing TRADE")
                                print2file(
                                    "MKT  order filled...FALSE TREND SIGNAL - Closing TRADE")
                                ib.disconnect()
                                in_position = False
                            else:

                                print(
                                    "1st-SNAP MID - FALSE TREND SIGNAL - Closing TRADE - order filled...")
                                print2file(
                                    "1st-SNAP MID - FALSE TREND SIGNAL - Closing TRADE - order filled...")
                                ib.disconnect()
                                in_position = False
############################################################################################################################
# early stop loss - ADX CLOSING OPEN TRADE******************************
    ib.sleep(0.001)
    if in_position == True:
        if current_time() < close_time():
            if df['adx'].iloc[-1] > adx_close_level:
                if df['adx'] .iloc[-1] < df['adx'].iloc[-2]:  # up trend curent and previous false
                    positions = ib.positions()  # A list of positions, according to IB
                    for position in positions:
                        in_position = True  # True There is an open trade
                        contract = Contract(conId=position.contract.conId)
                        ib.qualifyContracts(contract)
                        # type of contract, put('P') or PUT('C')
                        right = position.contract.right
                        close_trade = ib.placeOrder(
                            contract, SPX_close_snap_mid_order)  # CLOSE Put Contract
                        print(
                            'ADX >adx_close_level AND down trending - Closing TRADE  Order Placed ...')
                        print2file(
                            'ADX >adx_close_level AND down trending- Closing TRADE  Order Placed ...')
                        ib.sleep(3)  # wait for 120 secs
                        print('1st sleep')
                        if close_trade.orderStatus.status != 'Filled':
                            # cancel order type 'Snap Mid'
                            ib.cancelOrder(SPX_close_snap_mid_order)
                            ib.sleep(0.0001)
                            # Modify order to snap BUY PUT order
                            close_trade = ib.placeOrder(
                                contract, SPX_close_mkt_order_mod)
                            in_position = False
                            print(
                                "MKT order filled...ADX >adx_close_level AND down trending - Closing TRADE")
                            print2file(
                                "MKT  order filled...ADX >adx_close_level AND down trending - Closing TRADE")
                            ib.disconnect()
                            in_position = False
                        else:
                            in_position = False
                            print(
                                "1st-SNAP MID - ADX >adx_close_level AND down trending- Closing TRADE - order filled...")
                            print2file(
                                "1st-SNAP MID - ADX >adx_close_level AND down trending - Closing TRADE - order filled...")
                            ib.disconnect()
                            in_position = False
############################################################################################################################
# close/Exit All Positions - END OF DAY - ALL-Normal
    ib.sleep(0.001)
    if in_position == True:
        if current_time() > close_time():  # close time is 13:57
            positions = ib.positions()  # A list of positions, according to IB
            for position in positions:
                in_position = True  # True There is an open trade before start of session
                contract = Contract(conId=position.contract.conId)
                ib.qualifyContracts(contract)
                print('Current contract in position at close time')
                print(contract)
            close_trade = ib.placeOrder(
                contract, SPX_close_snap_mid_order)  # CLOSE Call Contract
            print("End of Day - Closing Order is Placed")
            print2file("End of Day - Closing Order is Placed")
            ib.sleep(3)  # wait for 120 secs
            print('1st sleep')
            if close_trade.orderStatus.status != 'Filled':
                # cancel order type 'Snap Mid'
                ib.cancelOrder(SPX_close_snap_mid_order)
                ib.sleep(0.0001)
                # Modify order to snap BUY call order
                close_trade = ib.placeOrder(contract, SPX_close_mkt_order_mod)
                print("MKT order End of Days Position Closed...")
                print2file("MKT order End of Days Position Closed...")
                ib.disconnect()
                in_position = False
            else:
                print("4rd-SNAP MID End of Days Position Closed...")
                print2file("4rd-SNAP MID End of Days Position Closed...")
                ib.disconnect()
                in_position = False
############################################################################################################################
    # ib.sleep(0.001)
    #print("Open Range High (Ophigh):",Ophigh)
    #print("Open Range low (Oplow):",Oplow)
    #print("Previous day lastbar high:",prevday_lastbar_high)
    #print("Previous day lastbar low:",prevday_lastbar_low)
    print("Have a good day! :)")
    # updatesignal()
    # ib.sleep(25)
    #print('Trades', ib.trades())
    # print("test iloc",df['date'].iloc[df[ (df['date'].dt.hour == 7) & (df['date'].dt.minute == 30) ].date.idxmax()]) #  df['date'].iloc[78]
    #print("test iloc2",df['date'].iloc[78])

    if current_time() > end_order_time():
        print('No more new trade entries. End of day...:)...current time:',
              current_time())


# ****************************************************************************************
# %%
while True:

    main()
        # ib.sleep(0.0001)
        # ib.sleep(1000000)

        

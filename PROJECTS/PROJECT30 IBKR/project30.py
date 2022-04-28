# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from ib_insync import *
util.startLoop()
from time import sleep
import ta
import pandas as pd
from datetime import datetime
from ta import add_all_ta_features
from ta.utils import dropna
import schedule
import matplotlib.pyplot as plt
import time
from ta.volatility import BollingerBands,AverageTrueRange
from ta.trend import ADXIndicator
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_rows',None)# display all df table, even when too long
#Import math Library
import math
import numpy as np
import time


# %%
in_position=False



# %%

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=12) # paper trading
#ib.connect('127.0.0.1', 7496, clientId=12) # Real account trade

RUT = Index('RUT')
ib.qualifyContracts(RUT)
print(RUT)
ib.reqMarketDataType(4)
#marketDataType (int) One of:
#1 = Live           - the default
#2 = Frozen         - typically used for bid/ask prices after market close
#3 = Delayed        - if the username does not have live market data subscriptions
#4 = Delayed frozen - combination of types 2 & 3

#Request market data for symbol to get current traded price - Requesting a ticker can take up to 11 seconds.#
market_data = ib.reqMktData(RUT,'',False,False)
print(market_data)
ib.sleep(0.1) #Wait until data is in.
RUTValue = market_data.last  # current price of equity
print (RUTValue) # current price of symbol

#The following request fetches a list of option chains:
#chains = ib.reqSecDefOptParams(RUTValue.symbol(str), '', RUTValue.secType, RUTValue.conId)
chains = ib.reqSecDefOptParams('RUT', '', 'IND', '416888') # values got from *- print(RUT)

#These are four option chains that differ in exchange and tradingClass. The latter is 'SPX' for the monthly and 'SPXW' for the weekly options. 
#Note that the weekly expiries are disjoint from the monthly ones, so when interested in the weekly options the monthly options can be added as well.
#In this case we're only interested in the weekly (infact - daily) options trading on SMART:
chain = next(c for c in chains if c.tradingClass == 'RUTW' and c.exchange == 'SMART')
#print(chain)
#What we have here is the full matrix of expirations x strikes. From this we can build all the option contracts that meet our conditions:

strikes = [strike for strike in chain.strikes
        if strike % 5 == 0
        #and RUTValue - 20 < strike < RUTValue + 20]  # should be like 5 for live data, so it trades very close to ITM
        and RUTValue - 5 < strike < RUTValue + 5] # choose closest strike ITM
        #and 2156 - 5 < strike < 2151 + 5] # Manual add for testing, on weekends with no display of punderlying price infor
print(strikes)
expirations = sorted(exp for exp in chain.expirations)[:1] #Sort the expiration contracts and choose the last one, usually today's or 1 day, or 2 days - but last
print(expirations)
# PUTS
def put_contract():
        rights = ['P'] #rights = ['P', 'C'] # where to specify whether just PUTS or Call, or Both contracts
        #print(expirations)
        p_contracts = [Option('RUT', expiration, strike, right, 'SMART', tradingClass='RUTW')
                for right in rights
                for expiration in expirations
                for strike in strikes]
#        print(strikes)
        p_contracts = ib.qualifyContracts(*p_contracts)
        return p_contracts[0]
#CALLS
def call_contract():
        rights = ['C'] #rights = ['P', 'C'] # where to specify whether just PUTS or Call, or Both contracts
        #print(expirations)
        c_contracts = [Option('RUT', expiration, strike, right, 'SMART', tradingClass='RUTW')
                for right in rights
                for expiration in expirations
                for strike in strikes]
#        print(strikes)
        c_contracts = ib.qualifyContracts(*c_contracts)
        return c_contracts[0]

#Market Order - Modifying orders
rut_open_mkt_order_mod =Order(orderId = 0,orderType='MKT', action='BUY', totalQuantity=1, auxPrice=1)
rut_close_mkt_order_mod=Order(orderId = 0,orderType='MKT', action='SELL', totalQuantity=1, auxPrice=1)

# Snap Mid Order Type
rut_open_snap_mid_order  =Order(orderId = 0,orderType='SNAP MID', action='BUY', totalQuantity=1, auxPrice=0.05) # orderId =0 first order, so it can be refereced and cancelled
rut_close_snap_mid_order =Order(orderId = 0,orderType='SNAP MID', action='SELL', totalQuantity=1, auxPrice=0.05)

#def dmi_trend(df):
    # By default, there is no open trade
positions = ib.positions()  # A list of positions, according to IB
for position in positions:
    in_position = True  #True There is an open trade before start of session
    
    print('There is an open position. Look 4 sell opportunities...')
    contract = Contract(conId = position.contract.conId)
    ib.qualifyContracts(contract)
    print('Current contract in position')
    print(contract)
    #time.sleep(1)
    


# %%
def candle():
    bars = ib.reqHistoricalData(
        RUT,
        endDateTime='',
        durationStr='1200 S', #1500 S after testing, this is number to go 
        barSizeSetting='1 min',
        whatToShow='TRADES',
        useRTH=True,
        keepUpToDate=True,
    )
#print(util.df(bars ))

    df = pd.DataFrame(bars)
    #print(df.tail(10))
    last_row_index = len(df.index)-1
    previous_row_index = last_row_index-1
#df['timesstamp'] = pd.to_datetime(df['timestamp'],unit='ms')
#print(df)

# INDICATORS
#********************************************************************************************
#definition    - > BollingerBands(close: pandas.core.series.Series, window: int = 20, window_dev: int = 2, fillna: bool = False)
#Intepretation - > BollingerBands(close=df["Close"], window=20, window_dev=2)

#definition    - > ADXIndicator(high: pandas.core.series.Series, low: pandas.core.series.Series, close: pandas.core.series.Series, window: int = 14, fillna: bool = False)
#Intepretation - > ADXIndicator(close=df["high"],close=df["low"],close=df["close"],window=4)
#********************************************************************************************

    # Initialize Bollinger Bands Indicator
    bb_indicator = BollingerBands(df['close'])
    #df['upper_band'] = bb_indicator.bollinger_hband()
    #df['lower_band'] = bb_indicator.bollinger_lband()
    #df['bb_moving_avg'] = bb_indicator.bollinger_mavg()

    # Initialize  Directional Movement Indicator (DMI)  Indicator

    DMI_ndicator = ADXIndicator(high=df["high"],low=df["low"],close=df["close"],window=4)
    df['DMIPlus'] = DMI_ndicator.adx_pos()
    df['DMIMinus'] = DMI_ndicator.adx_neg()
    #df['previous_close'] =df['close'].shift(1)
    df['degDMIPlus'] =df['DMIPlus'] - df['DMIPlus'].shift(1) #+ve - upsloping, -ve - downsloping
    df['degDMIMinus'] =df['DMIMinus'] - df['DMIMinus'].shift(1) #determining slope of DMIMinus. A +VE value indicate a rising slope while -ve implies downward slope
    df['In_Uptrend'] = False # Ininitialize Uptrend signals
    df['In_Downtrend'] = False # Ininitialize Downtrend signals

#print(df)

# setting uptrend conditions
    for current in range(1,len(df.index)):
        previous = current-1
    #print(current)
#********************************************************************************************
# setting uptrend - CALL conditions
#********************************************************************************************
#                  Main Condition
        if df['DMIPlus'][current] > df['DMIMinus'][current]:             #DMIPlus > DMIMinus
            if df['DMIPlus'][current]>60:                                #DMIPlus > 60
                if df['DMIPlus'][current] > df['DMIPlus'][previous]: #rising slope of DMIPlus
                        df['In_Uptrend'][current] = True
        elif df['DMIPlus'][current] < df['DMIMinus'][current]:
            if df['DMIMinus'][current]>60:
                df['In_Uptrend'][current] = False #by default everything is false, so this line was unnecessary. Just here for aesthetics
        else:
            df['In_Uptrend'][current] = df['In_Uptrend'][previous]  # Maintain default

# 1 - Exceptions for Uptrend - TRUE - Not converging for stop
        if df['DMIPlus'][current]>df['DMIMinus'][current]: #DMI+ greater then DMI-
            if df['DMIPlus'][previous] > df['DMIPlus'][current]:          #down sloping DMI+         *****
                if df['DMIMinus'][previous] > df['DMIMinus'][current]:# ALSO downsloping DMI-    *****
                        if df['In_Uptrend'][previous] == True:# Applies only if trade was uptrend..
                                df['In_Uptrend'][current] = True                       

# 2 - Exceptions for Uptrend - TRUE - Not converging for stop
        if df['DMIPlus'][current]>df['DMIMinus'][current]: #DMI+ greater then DMI-
            if df['DMIPlus'][current] > df['DMIPlus'][previous]:           #Up sloping DMI+   *****
                if df['DMIMinus'][previous] > df['DMIMinus'][current]: #downsloping DMI-  *****
                        if df['In_Uptrend'][previous] == True:# Applies just if trade was uptrend..
                                df['In_Uptrend'][current] = True 

# 3 - Exceptions for Uptrend - TRUE - Not converging for stop
        if df['DMIPlus'][current]>df['DMIMinus'][current]: #DMI+ greater then DMI-
            if df['DMIPlus'][current] > df['DMIPlus'][previous]: #Up sloping DMI+                *****
                if df['DMIMinus'][current] > df['DMIMinus'][previous]:# ALSO up sloping DMI- *****
                        if df['In_Uptrend'][previous] == True:# Applies just if trade was uptrend
                                df['In_Uptrend'][current] = True 

# 4 - Exceptions for Uptrend - TRUE - below threshold to consider a reversal
        if df['DMIPlus'][current]>df['DMIMinus'][current]: #DMI+ greater then DMI-
            if df['DMIMinus'][current] < 10: #below threshold to consider a trend reversal                *****
                        if df['In_Uptrend'][previous] == True:# Applies just if trade was uptrend
                                df['In_Uptrend'][current] = True 

 # 5 - Exceptions for Uptrend - TRUE - below threshold to consider a reversal
        if df['DMIPlus'][current]>df['DMIMinus'][current]: #DMI+ greater then DMI-
            if df['DMIPlus'][current] > 60: # threshold to consider a real uptrend                *****
                df['In_Uptrend'][current] = True   

#********************************************************************************************
# setting Downtrend - PUT conditions (same condions as above but reversed)
#********************************************************************************************                                                                                         
#                  Main Condition for PUT
          
        if df['DMIMinus'][current] > df['DMIPlus'][current]:
            if df['DMIMinus'][current]>60:
                if df['DMIMinus'][current] > df['DMIMinus'][previous]: #rising slope of DMIMinus
                        df['In_Downtrend'][current] = True
        elif df['DMIMinus'][current] < df['DMIPlus'][current]:
            if df['DMIPlus'][current]>60:
                df['In_Downtrend'][current] = False #by default everything is false, so this line was unnecessary. Just here for aesthetics
        else:
            df['In_Downtrend'][current] = df['In_Downtrend'][previous]


# 1 - Exceptions for Uptrend - TRUE - Not converging for stop
        if df['DMIMinus'][current]>df['DMIPlus'][current]: #DMI- greater then DMI+
            if df['DMIMinus'][previous] > df['DMIMinus'][current]:          #down sloping pppDMI-         *****
                if df['DMIPlus'][previous] > df['DMIPlus'][current]:# ALSO downsloping pppDMI+    *****
                        if df['In_Downtrend'][previous] == True:# Applies only if trade was uptrend
                                df['In_Downtrend'][current] = True                       

# 2 - Exceptions for Uptrend - TRUE - Not converging for stop
        if df['DMIMinus'][current]>df['DMIPlus'][current]: #DMI- greater then DMI+
            if df['DMIMinus'][current] > df['DMIMinus'][previous]:           #Up sloping DMI-   *****
                if df['DMIPlus'][previous] > df['DMIPlus'][current]: #downsloping pppDMI+  *****
                        if df['In_Downtrend'][previous] == True:# Applies just if trade was uptrend
                                df['In_Downtrend'][current] = True 

# 3 - Exceptions for Uptrend - TRUE - Not converging for stop
        if df['DMIMinus'][current]>df['DMIPlus'][current]: #DMI- greater then DMI+
            if df['DMIMinus'][current] > df['DMIMinus'][previous]: #Up sloping DMI-                *****
                if df['DMIPlus'][current] > df['DMIPlus'][previous]:# ALSO up sloping pppDMI+ *****
                        if df['In_Downtrend'][previous] == True:# Applies just if trade was uptrend
                                df['In_Downtrend'][current] = True 

# 4 - Exceptions for Uptrend - TRUE - below threshold to consider a reversal
        if df['DMIMinus'][current]>df['DMIPlus'][current]: #DMI- greater then DMI+
            if df['DMIPlus'][current] < 10: #below threshold to consider a trend reversal                *****
                        if df['In_Downtrend'][previous] == True:# Applies just if trade was uptrend
                                df['In_Downtrend'][current] = True 

 # 5 - Exceptions for Uptrend - TRUE - below threshold to consider a reversal
        if df['DMIMinus'][current]>df['DMIPlus'][current]: #DMI- greater then DMI+
            if df['DMIMinus'][current] > 60: # threshold to consider a real uptrend                *****
                df['In_Downtrend'][current] = True 

    print(f"downtrend is {df['In_Downtrend'].iloc[-1]}")
    print(f"downtrend is {df['In_Downtrend'].iloc[-2]}")
    print(df[-7:-1])
    return df[:-1]


# %%
df=candle()
if in_position==False:
    if df['In_Uptrend'].iloc[-1]==True:
        trade =   ib.placeOrder(call_contract(), rut_open_snap_mid_order)
        print("Order is Placed")
        ib.sleep(10) # wait for211, the logic for closing a trade 15 secs
        
        if trade.orderStatus.status !='Filled':  # if first order type"SNAP MID" is not filled, then get ready                               #
            ib.cancelOrder(rut_open_snap_mid_order) # cancel order
            ib.sleep(0.0001)
            trade =   ib.placeOrder(call_contract(), rut_open_mkt_order_mod) #Modify order, place market BUY Put order
            print(trade)
            in_position = True
        else:
            in_position = True
            print("Already in CALL position, nothing to do...")

    if df['In_Downtrend'].iloc[-1]==True:
        trade =   ib.placeOrder(put_contract(), rut_open_snap_mid_order)
        print("Order is Placed")
        ib.sleep(10)
            # wait for211, the logic for closing a trade 15 secs
        if trade.orderStatus.status !='Filled':  # if first order type"SNAP MID" is not filled, then get ready                               #
            ib.cancelOrder(rut_open_snap_mid_order) # cancel order
            ib.sleep(0.0001)
            trade =   ib.placeOrder(put_contract(), rut_open_mkt_order_mod) #Modify order, place market BUY Put order
            print(trade)
            in_position = True
        else:
            in_position = True
            print("Already in PUT position, nothing to do...")





def main():
    global in_position
    df=candle()
    print(in_position)
############################################################################################################################
    if in_position==False:
        if (df['In_Uptrend'].iloc[-1]==True and df['In_Uptrend'].iloc[-2]==False):
            trade =   ib.placeOrder(call_contract(), rut_open_snap_mid_order)
            print("Order is Placed")
            ib.sleep(10) # wait for211, the logic for closing a trade 15 secs
            
            if trade.orderStatus.status !='Filled':  # if first order type"SNAP MID" is not filled, then get ready                               #
                ib.cancelOrder(rut_open_snap_mid_order) # cancel order
                ib.sleep(0.0001)
                trade =   ib.placeOrder(call_contract(), rut_open_mkt_order_mod) #Modify order, place market BUY Put order
                print(trade)
                in_position = True
            else:
                in_position = True
                print("Already in CALL position, nothing to do...")

############################################################################################################################
    if in_position==False:
        if df['In_Downtrend'].iloc[-1]==True and df['In_Downtrend'].iloc[-2]==False:
            trade =   ib.placeOrder(put_contract(), rut_open_snap_mid_order)
            print("Order is Placed")
            ib.sleep(10)
             # wait for211, the logic for closing a trade 15 secs
            if trade.orderStatus.status !='Filled':  # if first order type"SNAP MID" is not filled, then get ready                               #
                ib.cancelOrder(rut_open_snap_mid_order) # cancel order
                ib.sleep(0.0001)
                trade =   ib.placeOrder(put_contract(), rut_open_mkt_order_mod) #Modify order, place market BUY Put order
                print(trade)
                in_position = True
            else:
                in_position = True
                print("Already in PUT position, nothing to do...")

############################################################################################################################
    if in_position==True:
        if df['In_Uptrend'].iloc[-1]==False and df['In_Uptrend'].iloc[-2]==True:
            positions = ib.positions()  # A list of positions, according to IB
            for position in positions:
                in_position = True  #True There is an open trade before start of session
                
                
                contract = Contract(conId = position.contract.conId)
                ib.qualifyContracts(contract)
                print('Current contract in position')
                print(contract)

            close_trade =   ib.placeOrder(contract, rut_close_snap_mid_order) #CLOSE Put Contract
            close_trade =  ib.placeOrder(contract, rut_close_snap_mid_order) #CLOSE Call Contract
            print("Order is Placed")
            ib.sleep(12) # wait for 15 secs
            if close_trade.orderStatus.status!='Filled':                              
                ib.cancelOrder(rut_close_snap_mid_order)
                ib.sleep(0.0001)
                #close_trade =   ib.placeOrder(call_contract(), rut_close_mkt_order_mod) #Modify order to snap BUY call order
                close_trade =   ib.placeOrder(contract, rut_close_mkt_order_mod) #Modify order to snap BUY call order
                print(close_trade)
                in_position = False
            else:
                in_position = False
                print("You are in a CALL position, nothing to Sell...")

############################################################################################################################
    if in_position==True:         

        if df['In_Downtrend'].iloc[-1]==False and df['In_Downtrend'].iloc[-2]==True:       
        #close_trade =   ib.placeOrder(put_contract(), rut_close_snap_mid_order) #CLOSE Put Contract
            positions = ib.positions()  # A list of positions, according to IB
            for position in positions:
                in_position = True  #True There is an open trade before start of session
                
                
                contract = Contract(conId = position.contract.conId)
                ib.qualifyContracts(contract)
                print('Current contract in position')
                print(contract)

            close_trade =   ib.placeOrder(contract, rut_close_snap_mid_order) #CLOSE Put Contract

            print("Order is Placed")
            ib.sleep(12) # wait for 10 secs
            if close_trade.orderStatus.status!='Filled':                              
                ib.cancelOrder(rut_close_snap_mid_order) #cancel order type 'Snap Mid'
                ib.sleep(0.0001)
                close_trade =   ib.placeOrder(contract, rut_close_mkt_order_mod) #Modify order to snap BUY put order
                print(close_trade)
                in_position = False
            else:
                in_position = False
                print("You are in PUT position, nothing to Sell...")


# %%
while True:


    main()
    time.sleep(14)




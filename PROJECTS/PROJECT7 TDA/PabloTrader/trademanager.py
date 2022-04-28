import math
import time
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from pandas.tseries.offsets import BDay
#import ast
#from enum import Enum
import pytz
from threading import Thread
#from termcolor import colored

from account import API_KEY, ACCOUNT_ID, REFRESH_TOKEN
from account import get_access_token

from TDAmeritrader import get_price_history, get_price_history_recent, get_price_history_between_times
from TDAmeritrader import get_positions, get_symbol_positions
from TDAmeritrader import get_quote, get_quotes, option_chain, GetATMOption, place_order

from datahandler import get_backdata, create_candle, update_candles

#from techlib import SMA, EMA, HullMA, calc_volatility, calc_psar
#from strategylib import ma_breakout_strategy, mean_reversion_strategy, chori_strategy, bros24_strategy
#from strategylib import get_state

from strategylib import run_backtest, run_live, run_backtest_OHLC


from authentication import generate_refresh_token

        
        
def tick_data(param):
    RUN_FOR_MINUTES = param['RUN_FOR_MINUTES']
    UPDATE_TICK_DATA_SECONDS = param['UPDATE_TICK_DATA_SECONDS']
    instrument_symbol_list = param['instrument_symbol_list']
    
    global g_tick_dict
    g_tick_dict = {}
    
    try:
        ACCESS_TOKEN = get_access_token()    
    except:
        print('access token fetch failed')
            
    i=0
    i_acc=0
    RUN_FOR_SECONDS = param['RUN_FOR_MINUTES']*60
    while(i<param['RUN_FOR_MINUTES']*60):
        time.sleep(UPDATE_TICK_DATA_SECONDS)
        i+=UPDATE_TICK_DATA_SECONDS
        #print("T1: ",datetime.now())  
        try:
            if i%900==0 or i_acc==1: ACCESS_TOKEN = get_access_token()
            i_acc=0    
        except:
            print('access token fetch failed')
            i_acc=1
        #print("T2: ",datetime.now())  
        try:
            g_tick_dict=get_quotes(ACCESS_TOKEN, instrument_symbol_list)
        except:
            print('quote fetch failed, handled')
        #print("T3: ",datetime.now())  
    print('Exiting quote fetch thread')
    return    
                        
                        

def live_trade(portfolio_dict, param, candles_dict):
    RUN_FOR_MINUTES = param['RUN_FOR_MINUTES']
    UPDATE_TICK_DATA_SECONDS = param['UPDATE_TICK_DATA_SECONDS']
    TRADE_LIVE = param['TRADE_LIVE']
    ALLOW_SHORT = param['ALLOW_SHORT']
    PLACE_ORDER = param['PLACE_ORDER']
    LOT_dict = param['LOT_dict']
    
    instrument_symbol_list = param['instrument_symbol_list']
    timeframe = param['timeframe']
    frequency = param['frequency']
    extended_hours = param['extended_hours']
    
    now = datetime.now()
    new_now = now
    old_minute=now.minute-1
    i=0
    acc_i=0
    candles_live=None
    
    space_='\t \t \t'

    newbar_dict = dict.fromkeys(instrument_symbol_list, False)
    for key in newbar_dict:
        newbar_dict[key] = not (now.minute==candles_dict[key][-1]['datetime'].minute)

    #g_tick_dict = {}
    tick_thread = Thread(target=tick_data,args=(param,))
    tick_thread.start()
    
    
    #for g in g_tick: g_tick_dict[instrument_symbol_list[instrument_token_list.index(g['instrument_token'])]] = g    
    if RUN_FOR_MINUTES>0:
        try:
            ACCESS_TOKEN = get_access_token()
            #g_tick_dict=get_quotes(ACCESS_TOKEN, instrument_symbol_list)
        except:
            print('Initial access token generation, returning, try again')
            return
                
    last_date = {}
    last_open = {}
    last_high = {}
    last_low = {}
    last_close = {}
    last_volume = {}

    exit_flag=0

    #print(now)
    print("loop BEGINS")
    while(i<param['RUN_FOR_MINUTES']):
        now = datetime.now()
        new_minute=now.minute
        new_second = now.second
        if new_minute!=old_minute:
            new_now = now
            print(now)
            
            try:
                if i%15==0 or i_acc==1: ACCESS_TOKEN = get_access_token()
                i_acc=0    
            except:
                print('access token fetch failed')
                i_acc=1

            #print("1: ",datetime.now())    
            i+=1
            #exit_flag=0
            old_minute = new_minute

            for key in g_tick_dict.keys():
                val = g_tick_dict[key]
                last_date_ = datetime.fromtimestamp(val['tradeTimeInLong']/1000)
                #UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()
                #last_date[key] = (last_date_ + UTC_OFFSET_TIMEDELTA).tz_localize('UTC').tz_convert('US/Eastern').replace(tzinfo=None)
                tz = pytz.timezone('US/Eastern')
                last_date[key]=last_date_.astimezone(tz)

                last_open[key] = val['lastPrice']
                last_high[key] = val['lastPrice']
                last_low[key] = val['lastPrice']
                last_close[key] = val['lastPrice']
                last_volume[key] = val['totalVolume']
                #print("V: ",val)
            #print("2: ",datetime.now())
            
            
            '''
            update recent history in first live candle
            '''
            #---------------------------------------------------------------------------------------------------------------
            if i==-1:
                hisD_dict = {}
                start_index_dict = {}
                
                for symbol in instrument_symbol_list:
                    #hisD_dict[symbol] = kite.historical_data(instrument_token_dict[symbol],to_date,to_date,interval)
                    df = None
                    try:
                        df = get_price_history_recent(symbol=symbol, intervals=60,
                                                frequencyType=timeframe, frequency=frequency,
                                                needExtendedHoursData=extended_hours, access_token=ACCESS_TOKEN)
                    except:
                        print("failed to fetch recent data")
                        continue
                    
                    hisD_dict[symbol] =df.to_dict('records')

                    #print("H: ",hisD_dict[symbol][-1]['high'])
                    
                    candles = candles_dict[symbol]
                    hiscandles = hisD_dict[symbol]
                    
                    #candleslen = len(candles)
                    lasttimestamp = candles[-1]['datetime']
                    lasttimestamphour = lasttimestamp.hour
                    lasttimestampminute = lasttimestamp.minute
                    
                    hislen = len(hiscandles) 
                    lasttimestampflag = 1
                    for i in range(hislen):
                        tmstmp = hiscandles[i]['datetime']
                        thr = tmstmp.hour
                        tmn = tmstmp.minute
                        if thr==lasttimestamphour and tmn==lasttimestampminute:
                            lasttimestampflag = 1
                            continue
                        
                        if lasttimestampflag == 1 and portfolio+symbol not in start_index_dict.keys():
                            start_index_dict[portfolio+symbol] = len(candles)     
                        
                        if lasttimestampflag == 1:
                            candles.append(hiscandles[i])
                
                print("start_index_dict:", start_index_dict)
                
                #print("2a: ",datetime.now())
                
                for portfolio in portfolio_dict.keys():
                    symbols = portfolio_dict[portfolio]
                    for symbol in symbols.keys():
                        if portfolio+symbol not in start_index_dict.keys():
                            continue    
                        candles_dict[symbol] = run_backtest_OHLC(portfolio_dict, portfolio, symbol,\
                                                                 candles_dict[symbol], param,\
                                                                 start_index_dict[portfolio+symbol])
            #---------------------------------------------------------------------------------------------------------------------
            
            #print("2b: ",datetime.now())  
            
            
            for symbol in instrument_symbol_list:
                if symbol in g_tick_dict.keys():
                    key=symbol
                    #print("gtick symbol:",candles_dict[symbol][-1])
                    hisD = [{'datetime':candles_dict[symbol][-1]['datetime'],'open':last_open[key],'high':last_high[key],
                             'low':last_low[key],'close':last_close[key],'volume':last_volume[key]}]
                    candles_dict[key], new_bar = update_candles(new_now, hisD, candles_dict[key], append=True, useoffset=False)
                    
            #print("3: ",datetime.now())   

            for portfolio in portfolio_dict.keys():
                symbols = portfolio_dict[portfolio]
                for symbol in symbols.keys():
                    candles_dict[symbol] = run_live(portfolio_dict, portfolio, symbol, candles_dict[symbol], param)
            
            #print("4: ",datetime.now())
            
            for portfolio in portfolio_dict.keys():
                symbols = portfolio_dict[portfolio]
                for symbol in symbols.keys():
                    candles_live = candles_dict[symbol]
                    
                    msg = portfolio+":"+symbol+" : " +str(candles_live[-1]['datetime'])+' '+str(candles_live[-1]['close'])\
                            +' '+str(candles_live[-1][portfolio+'trade_in'])+' '+str(candles_live[-2][portfolio+'trade_in'])
                    #print(symbol," : " ,candles_live[-1]['datetime'], candles_live[-1]['close'], 
                    #      candles_live[-1][portfolio+'trade_in'], candles_live[-2][portfolio+'trade_in'])
                    print(msg)
                    param['live_output']+=str(msg)
        
            'write live output '
            write_thread = Thread(target=write_live_output, args=(portfolio_dict, candles_dict, param, i,))
            write_thread.start()
        
        if True:
            for portfolio in portfolio_dict.keys():
                symbols = portfolio_dict[portfolio]
                for symbol in symbols.keys():
                    candles_live = candles_dict[symbol]
                        
                    #HARDCODE FOR TEST
                    #if i==2:
                    #    portfolio_dict[portfolio][symbol]['trade_in']=1
                    #    portfolio_dict[portfolio][symbol]['position']=3
                    
                    #----------------------place long orders--------------------------------------------------------------------
                    
                    if i>0 and portfolio_dict[portfolio][symbol]['trade_in']==1\
                            and candles_live[-2][portfolio+'trade_in']==0\
                            and portfolio_dict[portfolio][symbol]['inTrade'] == 0:
                        portfolio_dict[portfolio][symbol]['inTrade'] = 1
                        print(("Entry LONG: "+portfolio+":"+symbol\
                               +' Price:'+str(portfolio_dict[portfolio][symbol]['entryprice'])).rjust(100))    
                    
                        if PLACE_ORDER:
                                curPos=0
                                try:
                                    curPosDict = get_symbol_positions(symbol)
                                    #print("curPosDict ",curPosDict)
                                    if curPosDict is not None:
                                        curPos = curPosDict['longQuantity']
                                except:
                                    pass
                                if curPos == 0:
                                    pos = portfolio_dict[portfolio][symbol]['position']
                                    rec = place_order(ACCESS_TOKEN, symbol, pos, "BUY", "EQUITY", "MARKET")
                                portfolio_dict[portfolio][symbol]['tradeposition'] = portfolio_dict[portfolio][symbol]['position']
                    #-------------------------------------------------------------------------------------------------------------
                    
                    #--------------------place short orders-------------------------------------------------------------------
                    if i>0  and portfolio_dict[portfolio][symbol]['trade_in']==-1\
                                                and candles_live[-2][portfolio+'trade_in']==0\
                                                and portfolio_dict[portfolio][symbol]['inTrade'] == 0:
                        portfolio_dict[portfolio][symbol]['inTrade'] = -1
                        print(("Entry SHORT: "+portfolio+":"+symbol\
                               +' Price:'+str(portfolio_dict[portfolio][symbol]['entryprice'])).rjust(100))
                        if PLACE_ORDER:
                            curPos=0
                            try:
                                curPosDict = get_symbol_positions(symbol)
                                if curPosDict is not None:
                                    curPos = curPosDict['shortQuantity']
                            except:
                                pass
                            if curPos == 0:
                                pos = portfolio_dict[portfolio][symbol]['position']
                                rec = place_order(ACCESS_TOKEN, symbol, pos, "SELL_SHORT", "EQUITY", "MARKET")
                            portfolio_dict[portfolio][symbol]['tradeposition'] = portfolio_dict[portfolio][symbol]['position']
                    #----------------------------------------------------------------------------------------------------------        
            #print("5: ",datetime.now())
            
            #print("6: ",datetime.now())
        if True:
            ' intrabar update'
            if candles_live is None:
                #print("candle_live is None")
                time.sleep(60-new_second)
                continue
            else:
                time.sleep(UPDATE_TICK_DATA_SECONDS)

            
            for key in g_tick_dict.keys():
                try:
                    val = g_tick_dict[key]    
                    #last_date[key] = datetime.fromtimestamp(val['tradeTimeInLong']/1000)
                    last_date_ = datetime.fromtimestamp(val['tradeTimeInLong']/1000)
                    #UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()
                    #last_date[key] = (last_date_ + UTC_OFFSET_TIMEDELTA).tz_localize('UTC').tz_convert('US/Eastern').replace(tzinfo=None)
                    tz = pytz.timezone('US/Eastern')
                    last_date[key]=last_date_.astimezone(tz)

                    last_open[key] = last_open[key] if key in last_open.keys() else val['lastPrice']
                    last_high[key] = max(last_high[key],val['lastPrice']) if key in last_open.keys() else val['lastPrice']
                    last_low[key] = min(last_low[key],val['lastPrice']) if key in last_open.keys() else val['lastPrice']
                    last_close[key] = val['lastPrice']
                    last_volume[key] = val['totalVolume']
                    
                    #print("Qi: ",last_high[key] , last_low[key], last_close[key])
                except:
                    continue

                hisD = [{'datetime':last_date[key],'open':last_open[key],'high':last_high[key],
                         'low':last_low[key],'close':last_close[key],'volume':last_volume[key]}]

                
                candles_dict[key], new_bar = update_candles(new_now, hisD, candles_dict[key], append=False, useoffset=False)
                #newbar_dict[key] = False
 
            
            for portfolio in portfolio_dict.keys():
                symbols = portfolio_dict[portfolio]
                for symbol in symbols.keys():
                    candles_dict[symbol] = run_live(portfolio_dict, portfolio, symbol, candles_dict[symbol], param)

                
            for portfolio in portfolio_dict.keys():
                symbols = portfolio_dict[portfolio]
                for symbol in symbols.keys():
                    candles_live  = candles_dict[symbol]
                    #-------------------long exit--------------------------------------------------------
                    if portfolio_dict[portfolio][symbol]['trade_in']>=0\
                            and portfolio_dict[portfolio][symbol]['inTrade']>0\
                            and portfolio_dict[portfolio][symbol]['trade_in']!=portfolio_dict[portfolio][symbol]['inTrade']:
                        portfolio_dict[portfolio][symbol]['inTrade'] = portfolio_dict[portfolio][symbol]['trade_in']
                        print(("Exit LONG: "+str(portfolio_dict[portfolio][symbol]['trade_in'])\
                               +":"+portfolio+":"+symbol+' Price:'+str(portfolio_dict[portfolio][symbol]['exitprice'])).rjust(100))
                        #print("intradecount: ",portfolio_dict[portfolio][symbol]['intradecount'])
                        if PLACE_ORDER:
                            curPos=0
                            try:
                                curPosDict = get_symbol_positions(symbol)
                                if curPosDict is not None:
                                    curPos = curPosDict['longQuantity']
                            except:
                                pass
                            if curPos != 0:
                                pos = portfolio_dict[portfolio][symbol]['tradeposition'] - portfolio_dict[portfolio][symbol]['position']
                                rec = place_order(ACCESS_TOKEN, symbol, pos, "SELL", "EQUITY", "MARKET")
                            portfolio_dict[portfolio][symbol]['tradeposition'] = portfolio_dict[portfolio][symbol]['position']    
                    #-------------------short exit--------------------------------------------------------
                    if portfolio_dict[portfolio][symbol]['trade_in']<=0\
                            and portfolio_dict[portfolio][symbol]['inTrade']<0\
                            and portfolio_dict[portfolio][symbol]['trade_in']!=portfolio_dict[portfolio][symbol]['inTrade']:
                        portfolio_dict[portfolio][symbol]['inTrade'] = portfolio_dict[portfolio][symbol]['trade_in']
                        print(("Exit SHORT: "+str(portfolio_dict[portfolio][symbol]['trade_in'])\
                               +":"+portfolio+":"+symbol+' Price:'+str(portfolio_dict[portfolio][symbol]['exitprice'])).rjust(100))
                        #print(("Exit SHORT: "+symbol+' Price:'+str(portfolio_dict[portfolio][symbol]['exitprice'])).rjust(100))
                        #print("intradecount: ",portfolio_dict[portfolio][symbol]['intradecount'])
                        if PLACE_ORDER:
                            curPos=0
                            try:
                                curPosDict = get_symbol_positions(symbol)
                                if curPosDict is not None:
                                    curPos = curPosDict['shortQuantity']
                            except:
                                pass
                            if curPos != 0:
                                pos = portfolio_dict[portfolio][symbol]['tradeposition'] - portfolio_dict[portfolio][symbol]['position']
                                rec = place_order(ACCESS_TOKEN, symbol, pos, "BUY_TO_COVER", "EQUITY", "MARKET")
                            portfolio_dict[portfolio][symbol]['tradeposition'] = portfolio_dict[portfolio][symbol]['position']
                
    param['RUN_FOR_MINUTES'] = 0
    tick_thread.join()
    print("loop ENDS")        






def run_system(param=None, backdata=None):
    if param['generate_refresh_token'] is True:
        try:
            token = generate_refresh_token()
        except:
            print('refresh token generation falied, exiting, try again')
            return
    
    
    
    instrument_symbol_list = [] #param['instrument_symbol_list']
    for portfolio in param['portfolio_dict'].keys():
        symbols = param['portfolio_dict'][portfolio]
        for symbol in symbols.keys():
            if symbol not in instrument_symbol_list:
                instrument_symbol_list.append(symbol)
    param['instrument_symbol_list'] =  instrument_symbol_list       
    print('portfolio symbol unique list:',param['instrument_symbol_list'])        
    
    
    
    
    for symbol in instrument_symbol_list:
        if symbol not in param['LOT_dict'].keys():
            #print(symbol+" not found in lot dictionary, assigning unit value")
            param['LOT_dict'][symbol] = 1
            #return None
    
    for symbol in instrument_symbol_list:
        if symbol not in param['useVolatility_dict'].keys():
            #print(symbol+" not found in useVolatility dictionary, assigning True value")
            param['useVolatility_dict'][symbol] = True
            #return None
            
    
    RUN_FOR_MINUTES = param['RUN_FOR_MINUTES']
    UPDATE_TICK_DATA_SECONDS = param['UPDATE_TICK_DATA_SECONDS']
    TRADE_LIVE = param['TRADE_LIVE']
    ALLOW_SHORT = param['ALLOW_SHORT']
    PLACE_ORDER = param['PLACE_ORDER']
    LOT_dict = param['LOT_dict']
    
    
    timeframe = param['timeframe']
    frequency = param['frequency']
    extended_hours = param['extended_hours']
    periodType = param['periodType']
    period = param['period']
    
    if RUN_FOR_MINUTES>0:
        param['period'] = '3'
        period = param['period']    
            
    
    
    
    candles_dict = None
    candles15_dict = None
    candles30_dict = {}
    candles60_dict = {}
    candles240_dict = {}
    
    if backdata is None:
        historyData_dict, history15Data_dict, h30, h60, h240 = get_backdata(param)
        if historyData_dict is None:
            return None
        
        ''' create detailed candle properties '''
        candles_dict = historyData_dict.copy()
        candles15_dict = history15Data_dict.copy()
        
        if param['multiframe'] == True:
            candles30_dict = h30.copy()
            candles60_dict = h60.copy()
            candles240_dict = h240.copy()
        else:
            for symbol in instrument_symbol_list:
                candles30_dict[symbol] = None
                candles60_dict[symbol] = None
                candles240_dict[symbol] = None
        
        for symbol in instrument_symbol_list:
            for candle_ in candles_dict[symbol]:
                candle_ = create_candle(candle_)
    else:
        candles_dict = backdata.copy()
        for symbol in instrument_symbol_list:
            for candle_ in candles_dict[symbol]:
                candle_ = create_candle(candle_)
        

    '''
    portfolio initialization
    '''    
    portfolio_dict = None    
    portfolio_dict =  param['portfolio_dict'].copy()
    for portfolio in portfolio_dict.keys():
        symbols = portfolio_dict[portfolio]
        for symbol in symbols.keys():
            security = portfolio_dict[portfolio][symbol]
            security['index'] = -1
            security['trade_in'] = 0
            security['inTrade'] = 0
            security['intradecount'] = 0
            security['position'] = 0
            security['tradeposition'] = 0
            security['entryprice'] = 0.0
            security['exitprice'] = 0.0
            security['tradeprice'] = 0.0
            security['signal'] = []
            security['long_signal_fired'] = 0
            security['close_long_signal_fired'] = 0
            security['short_signal_fired'] = 0
            security['close_short_signal_fired'] = 0


    
            
    ''' prepare data for entire history'''
    for portfolio in portfolio_dict.keys():
        symbols = portfolio_dict[portfolio]
        for symbol in symbols.keys():
            #candles = candles_dict[symbol].copy()
            #candles_dict[symbol] = run_backtest(portfolio_dict, portfolio, symbol, candles_dict[symbol], param)
            candles_dict[symbol] = run_backtest_OHLC(portfolio_dict, portfolio, symbol, candles_dict[symbol],candles15_dict[symbol],\
                                                     candles30_dict[symbol],candles60_dict[symbol],candles240_dict[symbol],param)
            #print(candles_dict[symbol][10])

    
    
    
    
    ''' run live trade system '''    
    if RUN_FOR_MINUTES>0:
        live_trade(portfolio_dict, param, candles_dict, candles15_dict)

    
  
    
    #for symbol in instrument_symbol_list:
    for portfolio in portfolio_dict.keys():
        symbols = portfolio_dict[portfolio]
        for symbol in symbols.keys():    
            candles = candles_dict[symbol]
            for c in range(len(candles)):
                c0 = candles[c]
                c1 = candles[c-1]
                
                c0[portfolio+'trade_signal'] = 0
                c0[portfolio+'trade_signal_type'] = ''
                c0[portfolio+'tradeprice'] = 0.0
                c0[portfolio+'net_PnL'] = 0.0
                    
                if c0[portfolio+'trade_in']>0 and c1[portfolio+'trade_in']==0:
                    c0[portfolio+'trade_signal'] = 1
                    c0[portfolio+'trade_signal_type'] = 'BUY'
                    c0[portfolio+'tradeprice'] = c0[portfolio+'entryprice']
                elif c0[portfolio+'trade_in']<0 and c1[portfolio+'trade_in']==0:
                    c0[portfolio+'trade_signal'] = -1
                    c0[portfolio+'trade_signal_type'] = 'SHORT'
                    c0[portfolio+'tradeprice'] = c0[portfolio+'entryprice']
                elif c0[portfolio+'trade_in']!=c1[portfolio+'trade_in'] and c1[portfolio+'trade_in']>0:
                    c0[portfolio+'trade_signal'] = 2
                    c0[portfolio+'trade_signal_type'] = 'SELL'
                    c0[portfolio+'tradeprice'] = c0[portfolio+'exitprice']
                    c0[portfolio+'net_PnL'] = c0[portfolio+'sum_PnL_long_trades']
                elif c0[portfolio+'trade_in']!=c1[portfolio+'trade_in'] and c1[portfolio+'trade_in']<0:
                    c0[portfolio+'trade_signal'] = -2
                    c0[portfolio+'trade_signal_type'] = 'COVER'
                    c0[portfolio+'tradeprice'] = c0[portfolio+'exitprice']
                    c0[portfolio+'net_PnL'] = c0[portfolio+'sum_PnL_short_trades']
                else:
                    c0[portfolio+'trade_signal'] = 0
                    
    
    print("------------Equity Backtest Analysis------------")
    backtest_analysis_dict={}
    ''' post process file '''
    for portfolio in portfolio_dict.keys():
        backtest_analysis_dict[portfolio] = {}
        symbols = portfolio_dict[portfolio]
        for symbol in symbols.keys():
            backtest_analysis_dict[portfolio][symbol] = {}
            ba = backtest_analysis_dict[portfolio][symbol]
            if True:
                security = symbols[symbol]
                    
                dfsignal = pd.DataFrame(security['signal'])
                
                #if param['tradeDirection'] == 'LONG':
                if 'Short' not in dfsignal.columns:
                    dfsignal['Short'] = ''
                    dfsignal['CloseShort'] = ''
                    dfsignal['ShortPrice'] = ''
                    dfsignal['CloseShortPrice'] = ''
                    dfsignal['ShortPriceTime'] = ''
                
                #if param['tradeDirection'] == 'SHORT':
                if 'Long' not in dfsignal.columns:
                    dfsignal['Long'] = ''
                    dfsignal['CloseLong'] = ''
                    dfsignal['LongPrice'] = ''
                    dfsignal['CloseLongPrice'] = ''
                    dfsignal['LongPriceTime'] = ''     
                
                
                #print(dfsignal.head())
                dfsignal[['LongPrice','ShortPrice']] = dfsignal[['LongPrice','ShortPrice']].fillna(method='ffill')
                #print(dfsignal.head())

                dfsignal['LongPriceTime'] = dfsignal[dfsignal['Long']==True]['datetime']
                dfsignal['ShortPriceTime'] = dfsignal[dfsignal['Short']==True]['datetime']
                dfsignal[['LongPriceTime','ShortPriceTime']] = dfsignal[['LongPriceTime','ShortPriceTime']].fillna(method='ffill')

                
                dfsignal['LongHoldingPeriod'] = (dfsignal[dfsignal['CloseLong']==True]['datetime']\
                                                -dfsignal[dfsignal['CloseLong']==True]['LongPriceTime'])
                dfsignal['ShortHoldingPeriod'] = (dfsignal[dfsignal['CloseShort']==True]['datetime']\
                                                -dfsignal[dfsignal['CloseShort']==True]['ShortPriceTime'])
                
                
                dfsignal['LongPosition'] = dfsignal[dfsignal['Long']==True]['position']
                dfsignal['ShortPosition'] = dfsignal[dfsignal['Short']==True]['position']
                #dfsignal[['LongPosition','ShortPosition']] = dfsignal[['LongPosition','ShortPosition']].fillna(method='ffill')
                
                
                dfsignal['lastposition'] = dfsignal['position'].shift(1)
                dfsignal['LongPnL'] = (dfsignal[dfsignal['CloseLong']==True]['lastposition'] - dfsignal[dfsignal['CloseLong']==True]['position'])*(dfsignal[dfsignal['CloseLong']==True]['CloseLongPrice']-dfsignal[dfsignal['CloseLong']==True]['LongPrice'])
                dfsignal['ShortPnL'] = -1*(dfsignal[dfsignal['CloseShort']==True]['lastposition'] - dfsignal[dfsignal['CloseShort']==True]['position'])*(dfsignal[dfsignal['CloseShort']==True]['CloseShortPrice']-dfsignal[dfsignal['CloseShort']==True]['ShortPrice'])
                
                
                #-----------writing postprocessed output
                dfsignal = dfsignal.reindex(columns=(list([a for a in dfsignal.columns if a != 'comment'])+['comment']  ))
                dfsignal.to_csv('./data/'+portfolio+"_"+symbol+'_POSTPROCESSED_BACKTEST.csv')
                
                
                ba['LongTradeCount'] = dfsignal[dfsignal['Long']==True]['Long'].count()
                ba['ShortTradeCount'] = dfsignal[dfsignal['Short']==True]['Short'].count()
                ba['TradeCount'] = dfsignal[dfsignal['Long']==True]['Long'].count()+dfsignal[dfsignal['Short']==True]['Short'].count()
                
                ba['LongPnL'] = round(dfsignal['LongPnL'].sum(),2)
                ba['ShortPnL'] = round(dfsignal['ShortPnL'].sum(),2)
                ba['PnL'] = round(dfsignal['LongPnL'].sum() + dfsignal['ShortPnL'].sum(),2)
                
                
                ba['LongPositionAvg'] = round(dfsignal['LongPosition'].mean(),2)
                ba['ShortPositionAvg'] = round(dfsignal['ShortPosition'].mean(),2)
                
                tmp=0
                try:
                    tmp = (dfsignal['LongPosition'].sum()+dfsignal['ShortPosition'].sum())\
                            /(dfsignal['LongPosition'].count()+dfsignal['ShortPosition'].count())
                except:
                    tmp=0
                backtest_analysis_dict[portfolio][symbol]['PositionAvg'] = round(tmp,2)
                
                
                ba['LongHoldPeriodAvg(min)'] = round(dfsignal['LongHoldingPeriod'].mean().total_seconds() / 60,2)
                ba['ShortHoldPeriodAvg(min)'] = round(dfsignal['ShortHoldingPeriod'].mean().total_seconds() / 60,2)
                tmp=0
                try:
                    tmp = (dfsignal['LongHoldingPeriod'].sum()+dfsignal['ShortHoldingPeriod'].sum())\
                            /(dfsignal['LongHoldingPeriod'].count()+dfsignal['ShortHoldingPeriod'].count())
                except:
                    tmp=0
                ba['HoldPeriodAvg(min)'] = round(tmp / np.timedelta64(1, 'm'),2)
                
               
                '''
                ba['WinLongTrade'] = dfsignal[dfsignal['LongPnL']>0]['LongPnL'].count()
                ba['WinShortTrade'] = dfsignal[dfsignal['ShortPnL']>0]['ShortPnL'].count()
                ba['WinTrade'] = dfsignal[dfsignal['LongPnL']>0]['LongPnL'].count()\
                                    + dfsignal[dfsignal['ShortPnL']>0]['ShortPnL'].count()
                
                
                ba['LossLongTrade'] = dfsignal[dfsignal['LongPnL']<=0]['LongPnL'].count()
                ba['LossShortTrade'] = dfsignal[dfsignal['ShortPnL']<=0]['ShortPnL'].count()
                ba['LossTrade'] = dfsignal[dfsignal['LongPnL']<=0]['LongPnL'].count()\
                                    + dfsignal[dfsignal['ShortPnL']<=0]['ShortPnL'].count()
                
                
                
                try:
                    ba['WinLongTradePercent'] = round(100*ba['WinLongTrade'] / ba['LongTradeCount'],2)
                except:
                    ba['WinLongTradePercent'] = 0
                try:    
                    ba['WinShortTradePercent'] = round(100*ba['WinShortTrade'] / ba['ShortTradeCount'],2)
                except:
                    ba['WinShortTradePercent'] = 0
                try:    
                    ba['WinTradePercent'] = round(100*ba['WinTrade']/ba['TradeCount'],2)
                except:
                    ba['WinTradePercent'] = 0
                '''
                
                
                
                print('\n\n')
                print('Backtest Analysis:'+portfolio+" : "+symbol)
                #print(ba)
                
                k=0
                r=0
                sr=''
                for key in ba.keys():
                    kk = 30*(k%3)+10
                    r = r+1 if k%3==0 else r
                    nl = '\n' if k%3==0 else ''
                    
                    tt = '\t\t\t\t' if r==2 or r==5 else '\t\t\t'
                    tt = '\t\t' if r==4 or r==7 else tt
                    #tt = '' if r==5 and k%3==2 else tt
                    
                    sr += (nl+key+":"+str(ba[key])+tt)
                    #print((key+":"+str(ba[key])+nl).ljust(kk)) 
                    k+=1
                print(sr)
                
                
                dfn = pd.DataFrame(candles_dict[symbol])
                dfn= dfn[dfn['close'] != 0.0]
                trade_cap = 0.01*security['trade_capital']*param['account_capital']
                size = math.floor(trade_cap/dfn.iloc[0]['open'])
                BuyNHold = round(size*(dfn.iloc[-1-RUN_FOR_MINUTES]['close'] - dfn.iloc[0]['open']), 2)
                print('BuyNHold Size: '+str(size), " BuyNHold Profit: "+str(BuyNHold) )

            else:
                print('Error writing postprocessed backtest for '+symbol+':'+portfolio)
    
    
    
    
    
    
    '''' write final output in files '''
    #backtest_list = ['datetime','trade_signal','trade_signal_type','tradeprice','net_PnL']
    for portfolio in portfolio_dict.keys():
        backtest_list = ['datetime',portfolio+'trade_signal',\
                         portfolio+'trade_signal_type',portfolio+'tradeprice',\
                         portfolio+'position',portfolio+'net_PnL','comment']
        pts = portfolio+'trade_signal'
        symbols = portfolio_dict[portfolio]
        for symbol in symbols.keys():
            security = symbols[symbol]
            try:
                #print(dfn[backtest_list])
                dfn = pd.DataFrame(candles_dict[symbol])
                dfn.to_csv('./data/'+symbol+'_RAW.csv')
                #dfn[backtest_list].to_csv('./data/'+symbol+'_BACKTEST.csv')
                #fn2 = dfn[backtest_list].loc[0:len(dfn)-1-RUN_FOR_MINUTES]
                #fn2.loc[fn2[pts]!=0].to_csv('./data/'+portfolio+"_"+symbol+'_EQUITY_BACKTEST.csv')
                
                dfsig = pd.DataFrame(security['signal'])
                dfsig = dfsig.reindex(columns=(list([a for a in dfsig.columns if a != 'comment'])+['comment']  ))
                dfsig.to_csv('./data/'+portfolio+"_"+symbol+'_BACKTEST.csv')
                
            except:
                print('Error writing backtest file for '+symbol)
    
    
    
    
    
    ''' trade analysis '''        
    #print("------------Equity Backtest Analysis------------")
    '''
    for portfolio in portfolio_dict.keys():
        print("\n \n Portfolio: ",portfolio)
        #backtest_list = ['datetime',portfolio+'trade_signal',portfolio+'trade_signal_type',portfolio+'tradeprice',portfolio+'net_PnL']
        #pts = portfolio+'trade_signal'
        symbols = portfolio_dict[portfolio]
        for symbol in symbols.keys():
            try:
                dfn = pd.DataFrame(candles_dict[symbol])
                dfn= dfn[dfn['close'] != 0.0]
                
                trade_cap = 0.01*portfolio_dict[portfolio][symbol]['trade_capital']*param['account_capital']
                size = math.floor(trade_cap/dfn.iloc[0]['open'])
                
                print("\n Symbol: ",symbol)
                
                back_equity_profit=round(dfn.loc[0:len(dfn)-1-RUN_FOR_MINUTES][portfolio+'PnL'].sum(),2)
                print("Strategy Equity Backtest Profit: "+str(back_equity_profit))
                
                BuyNHold = round(size*(dfn.iloc[-1-RUN_FOR_MINUTES]['close'] - dfn.iloc[0]['open']), 2)
                print('BuyNHold Size: '+str(size), " BuyNHold Profit: "+str(BuyNHold) )
            except:
                print('Error writing backtest analysis for '+symbol)
    '''
    
    
    return candles_dict, portfolio_dict, backtest_analysis_dict



def write_live_output(portfolio_dict, candles_dict, param, count):
    for portfolio in portfolio_dict.keys():
        backtest_list = ['datetime',portfolio+'trade_signal',\
                         portfolio+'trade_signal_type',portfolio+'tradeprice',\
                         portfolio+'position',portfolio+'net_PnL','comment']
        pts = portfolio+'trade_signal'
        symbols = portfolio_dict[portfolio]
        for symbol in symbols.keys():
            security = symbols[symbol]
            try:
                #print(dfn[backtest_list])
                dfn = pd.DataFrame(candles_dict[symbol])
                dfn.to_csv('./data/'+symbol+'_RAW.csv')
            except:
                print('live write output failed for '+symbol+" "+portfolio+',handled')
    
    return




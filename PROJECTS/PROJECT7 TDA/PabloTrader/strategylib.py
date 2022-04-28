import math
import numpy as np
from datetime import datetime
import pandas as pd

from techlib import SMA, EMA, HullMA, SMACandle, EMACandle, RSICandle
from techlib import SMACandleKey, EMACandleKey, HullMACandleKey, EMAKeyCandleKey
from techlib import getDailyData, getDailyDataOnCandle
from techlib import calc_volatility, calc_psar


from ma_breakout_strategy import ma_breakout_strategy


def get_state_analysis(symbol, candles, index, portfolio_dict, portfolio, param, live):
    candle = candles[index]
    security = portfolio_dict[portfolio][symbol]
    
    if index<1:
        candle[portfolio+'trade_in'] = 0
        candle[portfolio+'position'] = 0
        candle[portfolio+'entryprice'] = 0.0
        candle[portfolio+'exitprice'] = 0.0
        candle[portfolio+'exit_flag'] = 0
        candle[portfolio+'sum_PnL_long_trades'] = 0.0
        candle[portfolio+'sum_PnL_short_trades'] = 0.0
        return
    
    previous = candles[index-1]
    
    
    candle[portfolio+'trade_in'] = security['trade_in']
    candle[portfolio+'position'] = security['position']
    
    candle[portfolio+'entryprice'] = security['entryprice']
    candle[portfolio+'exitprice'] = security['exitprice']
    
    
    sgn = math.copysign(1,candle[portfolio+'trade_in'])
    sgn1 = math.copysign(1,previous[portfolio+'trade_in'])
    
    sgnentry = candle[portfolio+'trade_in'] != previous[portfolio+'trade_in'] and abs(candle[portfolio+'trade_in'])==1
    sgntrade = candle[portfolio+'trade_in'] == previous[portfolio+'trade_in'] and previous[portfolio+'trade_in']!=0
    sgnexit = candle[portfolio+'trade_in'] != previous[portfolio+'trade_in'] and previous[portfolio+'trade_in']!=0
    
    #print(candle[portfolio+'trade_in'], sgnentry, sgntrade, sgnexit)
    
    pos = candle[portfolio+'position']
    pos1 = previous[portfolio+'position']
    
    changePnL = sgn1*pos1*(candle[portfolio+'exitprice'] - previous['close']) + sgn*pos*(candle['close'] - candle[portfolio+'exitprice'])
    
    pnl = 0.0
    if sgnentry:
        pnl = sgn*pos*(candle['close']-candle[portfolio+'entryprice'])
        candle[portfolio+'sum_PnL_long_trades'] = pnl if sgn==1 else 0.0
        candle[portfolio+'sum_PnL_short_trades'] = pnl if sgn==-1 else 0.0
    elif sgntrade:
        pnl = sgn*pos*(candle['close']-previous['close'])
        candle[portfolio+'sum_PnL_long_trades'] = previous[portfolio+'sum_PnL_long_trades']+pnl  if sgn==1 else 0.0
        candle[portfolio+'sum_PnL_short_trades'] = previous[portfolio+'sum_PnL_short_trades']+pnl  if sgn==-1 else 0.0
    elif sgnexit:
        pnl = changePnL
        candle[portfolio+'sum_PnL_long_trades'] = previous[portfolio+'sum_PnL_long_trades']+pnl  if sgn==1 else 0.0
        candle[portfolio+'sum_PnL_short_trades'] = previous[portfolio+'sum_PnL_short_trades']+pnl  if sgn==-1 else 0.0
    else:
        pnl = 0.0
        candle[portfolio+'sum_PnL_long_trades'] =  0.0
        candle[portfolio+'sum_PnL_short_trades'] =  0.0
    
    #print(pnl)
    
    
    candle[portfolio+'PnL'] = pnl
    
    
    if 'stoplossprice' in security.keys():
        candle[portfolio+'stoplossprice'] = security['stoplossprice']
        
    if 'takeprofitprice' in security.keys():
        candle[portfolio+'takeprofitprice'] = security['takeprofitprice']
    
    return
        




def run_backtest(portfolio_dict, portfolio, symbol, candles, param):
    #if 'strategy' not in param.keys():
    #    print('strategy key missing')
    #    return
    
    print(portfolio, symbol)
    #useVolatility = True
    #if symbol in param['useVolatility_dict'].keys():
    #    useVolatility = param['useVolatility_dict'][symbol]
    
    portfolio_strategy = portfolio[symbol]['strategy']
    
    if portfolio_strategy == 'ma_breakout_strategy':
        df = pd.DataFrame(candles)
        for index,candle in enumerate(candles):
            candles[index] = ma_breakout_strategy(df, candles, index, param, portfolio)
            #0t_state(symbol, candles, index, portfolio_dict, portfolio, param, False)
    elif portfolio_strategy == 'mean_reversion_strategy':
        df = pd.DataFrame(candles)
        for index,candle in enumerate(candles):
            candles[index] = mean_reversion_strategy(df, candles, index, param, portfolio)
            #gtate(symbol, candles, index, portfolio_dict, portfolio, param, False)  
    else:
        print('incorrect strategy')
        return
    
    #candles = df.to_dict('records')
    for c in df.columns:
        if c not in candles[0].keys():
            for i in range(len(candles)):
                candles[i][c] = df.at[i,c]
    
    return candles





def run_backtest_OHLC(portfolio_dict=None, portfolio=None, symbol=None, candles=None,\
                      candles15=None, candles30=None, candles60=None,candles240=None,param=None, start_index=0):
    print(datetime.now(), portfolio, symbol)
    
    for i in range(len(candles15)):
        candles15[i]['rsi'] = RSICandle(candles15, i, 14)
        candles15[i]['rsisma'] = SMACandleKey(candles15, i, 10, 'rsi')
    
    '''
    if param['multiframe']==True:
        for i in range(len(candles30)):
            candles30[i]['SMA1'] = RSICandle(candles30, i, 14)
            candles30[i]['SMA10'] = SMACandleKey(candles30, i, 10, 'rsi')
    '''
    
    
    candles_slice = []
    candles15_slice = []
    candles30_slice = []
    candles60_slice = []
    candles240_slice = []
    
    if start_index!=0:
        for i in range(start_index):
            candle = candles[i]
            new_candle = candle.copy()
            candles_slice.append(new_candle)
        
    #candles[index-1]['high']*1.0001
    #candles[index-1]['low']*0.9999
    
    #for index, candle in enumerate(candles):
    
    end_index = len(candles)
    for index in range(start_index, end_index):    
        candle = candles[index]
        
        index15 = candle['index15']
        candle15 = candles15[index15]
        
        if param['multiframe']==True:
            candle30 = candles30[candle['index30']]
            candle60 = candles60[candle['index60']]
            candle240 = candles240[candle['index240']]
    
        intrabar = []
        
        if candle['close'] > candle['open']:
            #intrabar = ['C']
            intrabar = ['O','L','H','C']
            #intrabar = ['O','PL','L','PH','C','H','C']
            #intrabar = ['O','PL','PH','C']
        else:
            #intrabar = ['C']
            intrabar = ['O','H','L','C']
            #intrabar = ['O','PH','H','PL','C','L','C']
            #intrabar = ['O','PH','PL','C']
            
        for price in intrabar:
            #candles_copy = candle.copy()
            if price == 'O':
                new_candle = candle.copy()
                new_candle['close'] = new_candle['open']
                new_candle['high'] = new_candle['open']
                new_candle['low'] = new_candle['open']
                candles_slice.append(new_candle)
                
                new_candle15 = candle15.copy()
                new_candle15['close'] = new_candle['close']
                new_candle15['high'] = new_candle15['open']
                new_candle15['low'] = new_candle15['open']
                candles15_slice.append(new_candle15)
                
                if param['multiframe']==True:
                    new_candle30 = candle30.copy()
                    new_candle30['close'] = new_candle['close']
                    candles30_slice.append(new_candle30) 
                    
                    new_candle60 = candle60.copy()
                    new_candle60['close'] = new_candle['close']
                    candles60_slice.append(new_candle60)
                    
                    new_candle240 = candle240.copy()
                    new_candle240['close'] = new_candle['close']
                    candles240_slice.append(new_candle240)
                
            elif price == 'L':
                #new_candle = candle.copy()
                close = candle['low']
                high = max(close, candles_slice[-1]['high'])
                low = min(close, candles_slice[-1]['low'])
                candles_slice[-1]['close'] = close
                candles_slice[-1]['high'] = high
                candles_slice[-1]['low'] = low
                
                
                #close = candle15['low']
                high = max(close, candles15_slice[-1]['high'])
                low = min(close, candles15_slice[-1]['low'])
                candles15_slice[-1]['close'] = close
                candles15_slice[-1]['high'] = high
                candles15_slice[-1]['low'] = low
                
                if param['multiframe']==True:
                    candles30_slice[-1]['close'] = close
                    candles60_slice[-1]['close'] = close
                    candles240_slice[-1]['close'] = close
                
            elif price == 'C':
                #new_candle = candle.copy()
                close = candle['close']
                high = max(close, candles_slice[-1]['high'])
                low = min(close, candles_slice[-1]['low'])
                candles_slice[-1]['close'] = close
                candles_slice[-1]['high'] = high
                candles_slice[-1]['low'] = low
                
                #close = candle15['close']
                high = max(close, candles15_slice[-1]['high'])
                low = min(close, candles15_slice[-1]['low'])
                candles15_slice[-1]['close'] = close
                candles15_slice[-1]['high'] = high
                candles15_slice[-1]['low'] = low
                
                if param['multiframe']==True:
                    candles30_slice[-1]['close'] = close
                    candles60_slice[-1]['close'] = close
                    candles240_slice[-1]['close'] = close
                
            elif price == 'H':
                #new_candle = candle.copy()
                close = candle['high']
                high = max(close, candles_slice[-1]['high'])
                low = min(close, candles_slice[-1]['low'])
                candles_slice[-1]['close'] = close
                candles_slice[-1]['high'] = high
                candles_slice[-1]['low'] = low
                
                
                #close = candle15['high']
                high = max(close, candles15_slice[-1]['high'])
                low = min(close, candles15_slice[-1]['low'])
                candles15_slice[-1]['close'] = close
                candles15_slice[-1]['high'] = high
                candles15_slice[-1]['low'] = low
                
                if param['multiframe']==True:
                    candles30_slice[-1]['close'] = close
                    candles60_slice[-1]['close'] = close
                    candles240_slice[-1]['close'] = close
                
            elif price == 'PH':
                #new_candle = candle.copy()
                close = 1.00011*candles[index-1]['high']
                if close<candle['low'] or close>candle['high']: continue
                high = max(close, candles_slice[-1]['high'])
                low = min(close, candles_slice[-1]['low'])
                candles_slice[-1]['close'] = close
                candles_slice[-1]['high'] = high
                candles_slice[-1]['low'] = low
            elif price == 'PL':
                #new_candle = candle.copy()
                close = 0.99989*candles[index-1]['low']
                if close<candle['low'] or close>candle['high']: continue
                
                #print(candle)
                
                high = max(close, candles_slice[-1]['high'])
                low = min(close, candles_slice[-1]['low'])
                candles_slice[-1]['close'] = close
                candles_slice[-1]['high'] = high
                candles_slice[-1]['low'] = low    
            else:
                new_candle = candle.copy()
                new_candle['close'] = new_candle['close']
                new_candle['high'] = max(new_candle['close'], candles_slice[-1]['high'])
                new_candle['low'] = min(new_candle['close'], candles_slice[-1]['low'])
                candles_slice[-1]['close'] = new_candle['close']
                candles_slice[-1]['high'] = new_candle['high']
                candles_slice[-1]['low'] = new_candle['low']
            
            #if price == 'C':
            candles_slice = run_live(portfolio_dict, portfolio, symbol, candles_slice, candles15,candles30,candles60,candles240,param)
            #if price=='O' and index%100==0: print(index, candles_slice[index])
    return candles_slice



def run_live(portfolio_dict, portfolio, symbol, candles, candles15, candles30,candles60,candles240,param):
    #print(portfolio, symbol)
    #df = pd.DataFrame(candles)
    index = len(candles) - 1
    
    #print("portfolio:",portfolio)
    portfolio_strategy = portfolio_dict[portfolio][symbol]['strategy']
    
    if portfolio_strategy == 'ma_breakout_strategy':
        df = None
        ma_breakout_strategy(df, candles, candles15,candles30,candles60,candles240, index, param, symbol, portfolio, portfolio_dict, True)   
        get_state_analysis(symbol, candles, index, portfolio_dict, portfolio, param, True) 
    elif portfolio_strategy == 'mean_reversion_strategy':
        df = None
        mean_reversion_strategy(df, candles, index, param, symbol, portfolio, portfolio_dict, True)   
        get_state_analysis(symbol, candles, index, portfolio_dict, portfolio, param, True) 
    else:
        print('incorrect strategy')
        return
    
    return candles



import math
import numpy as np
from datetime import datetime
import pandas as pd

from techlib import SMACandleKey, EMAKeyCandleKey, Momentum, MomentumSMA, PVT, RSICandle

from timemanager import check_tradewindow, check_intraday_squareoff

def ma_breakout_strategy(df, candles, candles15, candles30,candles60,candles240, index, param, symbol, portfolio, portfolio_dict, live):
    candle = candles[index]
    
    index15 = candle['index15']
    candle15 = candles15[index15]
    
    if param['multiframe']==True:
        index30 = candle['index30']
        index60 = candle['index60']
        index240 = candle['index240']
        candle30 = candles30[candle['index30']]
        candle60 = candles60[candle['index60']]
        candle240 = candles240[candle['index240']]
    
    
    
    security =  portfolio_dict[portfolio][symbol]
    
    if portfolio+'trade' not in candle.keys():
        candle[portfolio+'trade'] = 0

    security['long_signal_fired'] = 0
    security['close_long_signal_fired'] = 0
    security['short_signal_fired'] = 0
    security['close_short_signal_fired'] = 0
    
    newbar=False
    if security['index'] != index:
        security['index'] = index
        newbar = True
    
    
    buy = portfolio+'_buy'
    sell = portfolio+'_sell'
    sellPrice = portfolio+'_sellPrice'

    short = portfolio+'_short'
    cover = portfolio+'_cover'
    coverPrice = portfolio+'_coverPrice'

    candle[buy] = False
    candle[sell] = False
    candle[short] = False
    candle[cover] = False
    
    
    #candle['SMA'] = EMAKeyCandleKey(candles, index, param['SMAPeriod'], 'close','SMA')
    #candle['EMA'] = EMAKeyCandleKey(candles, index, param['EMAPeriod'], 'close', 'EMA')
    #-------------------------------------------------------------------
    
    if index<1:
        candle['SMA1'] = candle['close']
        candle['SMA10'] = candle['close']
        candle['SMA15'] = candle['close']
        candle['SMA21'] = candle['close']
        candle['EMA15'] = candle['close']
        candle['EMA12'] = candle['close']
        candle['EMA26'] = candle['close']
        candle['momentum'] =  0.0
        candle['momentumSMA'] =  0.0
        candle['pvt'] = 0.0
        
        candle15['rsi'] =  0.0
        candle15['rsisma'] = 0.0
        
        candle['rsi15min'] = candle15['rsi'] 
        candle['rsisma15min'] = candle15['rsisma']
        
        return
    
    
    candle['SMA1'] = SMACandleKey(candles, index, 1, 'close')
    candle['SMA10'] = SMACandleKey(candles, index, 10, 'close')
    candle['SMA15'] = SMACandleKey(candles, index, 15, 'close')
    candle['SMA21'] = SMACandleKey(candles, index, 21, 'close')
    candle['EMA15'] = EMAKeyCandleKey(candles, index, 15, 'close', 'EMA15')
    
    
    
    mflong = True
    mfshort = True
    if param['multiframe']==True:
        candle30['SMA1'] = SMACandleKey(candles30, index30, 1, 'close')
        candle30['SMA10'] = SMACandleKey(candles30, index30, 10, 'close')
        
        candle60['SMA1'] = SMACandleKey(candles60, index60, 1, 'close')
        candle60['SMA10'] = SMACandleKey(candles60, index60, 10, 'close')
        
        candle240['SMA1'] = SMACandleKey(candles240, index240, 1, 'close')
        candle240['SMA10'] = SMACandleKey(candles240, index240, 10, 'close')
        
        candle['SMA1-30min'] = candle30['SMA1']
        candle['SMA10-30min'] = candle30['SMA10']
        
        candle['SMA1-60min'] = candle60['SMA1']
        candle['SMA10-60min'] = candle60['SMA10']
        
        candle['SMA1-240min'] = candle240['SMA1']
        candle['SMA10-240min'] = candle240['SMA10']
        
        mflong = candle30['SMA1'] > candle30['SMA10'] and candle60['SMA1'] > candle60['SMA10'] and candle240['SMA1'] > candle240['SMA10']
        mfshort = candle30['SMA1'] < candle30['SMA10'] and candle60['SMA1'] < candle60['SMA10'] and candle240['SMA1'] < candle240['SMA10']
    
    
    candle['momentum'] = Momentum(candles, index, 12)
    candle['momentumSMA'] = MomentumSMA(candles, index, 21)
    
    
    if param['multiframe']==True:
        trendUP = candle['SMA1'] > candle['SMA10']
    
        trendDN = candle['SMA1'] < candle['SMA10']
    else:
        trendUP = candle['EMA15'] > candle['SMA15'] \
              and  candle['SMA1'] > candle['SMA10']
    
        trendDN = candle['EMA15'] < candle['SMA15'] \
              and  candle['SMA1'] < candle['SMA10']
    
    
    triggerBuy = candle['momentum'] > candle['momentumSMA'] and  candles[index-1]['momentum'] < candles[index-1]['momentumSMA']\
                    and candle['momentum'] > 0 and candle['momentumSMA'] > 0
    
    triggerShort = candle['momentum'] < candle['momentumSMA'] and  candles[index-1]['momentum'] > candles[index-1]['momentumSMA']\
                    and candle['momentum'] < 0 and candle['momentumSMA'] < 0
    
    
    #dt = candle['datetime']
    #secondary_index = df15.index[df15.index.get_loc(dt, method='nearest')]
    
    #candle15['EMA12'] = EMAKeyCandleKey(candles15, index, 12, 'close', 'EMA12')
    #candle15['EMA26'] = EMAKeyCandleKey(candles15, index, 26, 'close', 'EMA26')
    #candle15['pvt'] = PVT(candles15, index)
    
    
    OB = 60
    OS = 45
    
    if index15<1:
        candle15['rsi'] =  0.0
        candle15['rsisma'] = 0.0
        
        candle['rsi15min'] = candle15['rsi']
        candle['rsisma15min'] = candle15['rsisma']
        
        sellCondition = False
        coverCondition = False
    else:
        candle15['rsi'] = RSICandle(candles15, index15, 14)
        candle15['rsisma'] = SMACandleKey(candles15, index15, 10, 'rsi')
    
        candle['rsi15min'] = candle15['rsi'] 
        candle['rsisma15min'] = candle15['rsisma']
        
        sc1 = candle15['rsi'] < candle15['rsisma'] and candles15[index15-1]['rsi'] > candles15[index15-1]['rsisma']\
                    and candle15['rsi'] > OB
        sc2 = candle15['rsi'] < OB and candles15[index15-1]['rsi'] > OB and candle15['rsisma'] < OB
        sellCondition = sc1 or sc2

        cc1 = candle15['rsi'] > candle15['rsisma'] and candles15[index15-1]['rsi'] < candles15[index15-1]['rsisma']\
                        and candle15['rsi'] < OS
        cc2 = candle15['rsi'] > OS and candles15[index15-1]['rsi'] < OS and candle15['rsisma'] > OS
        coverCondition = cc1 or cc2
    
    
    
    
    
    
    
    TPExit = False
    SLExit = False
    TSLExit = False
    
    PnL = 100*security['trade_in']*(candle['close'] - security['entryprice'])/candle['close'] if candle['close']!=0 else 0
    
    if param['RegularTargetProfit']>0:
        TPExit = param['RegularTargetProfit'] <= PnL
    
    if param['RegularStopLoss']>0:
        SLExit = param['RegularStopLoss'] <= -PnL
        
    #if param['TrailStopLoss']>0:
    #    TSLExit = param['RegularTargetProfit'] > PnL    
    
    
    #-------------------------------------------------------------------
    
    
    
    
    
    
    '''-----------------------------Signal calculations-----------------------'''   
    
    maxhist = 21
    if index < maxhist:
        return
    
    
    ''' buy signal '''    
    candle[buy] = trendUP and triggerBuy and mflong
    
    
    '''  sell signal '''
    candle[sell] = sellCondition
    candle[sellPrice] = candle['close']
    
    
    ''' short signal '''
    candle[short] = trendDN and triggerShort and mfshort
    
    
    ''' cover signal '''
    candle[cover] = coverCondition
    candle[coverPrice] = candle['close']


    '''----------------------------Trade-----------------------------------------'''
    squareoff = check_intraday_squareoff(symbol, candles, index, portfolio_dict, portfolio, param)
    if squareoff:
        return
    
    tradewindow = check_tradewindow(candles, index, param)
    
    
    
    ''' trade long '''
    if tradewindow and security['trade_in']==0 and candles[index][buy]  and candle[portfolio+'trade']==0:
        candle[portfolio+'trade']=1
        security['trade_in'] = 1
        security['entryprice'] = candle['close']
            
        trade_cap = 0.01*portfolio_dict[portfolio][symbol]['trade_capital']*param['account_capital']
        position = math.floor(trade_cap/security['entryprice'])
        security['position'] = position
    
        #security['stoplossprice'] = candle['minima1Price']
    
        comment = 'LONG strategy Entry: '+str(security['entryprice'])
        if param['show_detail_log']: print(str(candle['datetime'])+'\t'+comment)
        candle['comment']+=comment
        signal = {'datetime':candle['datetime'],'Long':True, 'LongPrice':security['entryprice'],\
                  'position':security['position'],'comment':comment,'SMA1':candle['SMA1'],'SMA10':candle['SMA10'],\
                 'SMA15':candle['SMA15'],'EMA15':candle['EMA15'],'momentum':candle['momentum'],\
                  'momentumPrev':candles[index-1]['momentum'],'momentumSMA':candle['momentumSMA'],\
                  'momentumSMAPrev':candles[index-1]['momentumSMA']}
        security['signal'].append(signal)
        
        
    
    if security['trade_in']>0 and candles[index][sell]:
        candle[portfolio+'trade']=0
        security['trade_in'] = 0
        security['exitprice'] = candle['close']
        security['position'] = 0
        
        
        comment = 'LONG strategy Exit: '+str(security['exitprice'])
        if param['show_detail_log']: print(str(candle['datetime'])+'\t'+comment)
        candle['comment']+=comment
        signal = {'datetime':candle['datetime'],'CloseLong':True, 'CloseLongPrice':security['exitprice'],\
                  'position':security['position'],'comment':comment}
        security['signal'].append(signal)
    elif security['trade_in']>0 and TPExit:
        candle[portfolio+'trade']=0
        security['trade_in'] = 0
        security['exitprice'] = candle['close']
        security['position'] = 0
        
        comment = 'LONG TargetProfit Exit: '+str(security['exitprice'])
        if param['show_detail_log']: print(str(candle['datetime'])+'\t'+comment)
        candle['comment']+=comment
        signal = {'datetime':candle['datetime'],'CloseLong':True, 'CloseLongPrice':security['exitprice'],\
                  'position':security['position'],'comment':comment}
        security['signal'].append(signal)     
    elif security['trade_in']>0 and SLExit:
        candle[portfolio+'trade']=0
        security['trade_in'] = 0
        security['exitprice'] = candle['close']
        security['position'] = 0
        
        comment = 'LONG StopLoss Exit: '+str(security['exitprice'])
        if param['show_detail_log']: print(str(candle['datetime'])+'\t'+comment)
        candle['comment']+=comment
        signal = {'datetime':candle['datetime'],'CloseLong':True, 'CloseLongPrice':security['exitprice'],\
                  'position':security['position'],'comment':comment}
        security['signal'].append(signal)     
        
    
    ''' trade short '''
    if tradewindow and security['trade_in']==0 and candles[index][short]  and candle[portfolio+'trade']==0:
        candle[portfolio+'trade'] = -1
        security['trade_in'] = -1
        security['entryprice'] = candle['close']
            
        trade_cap = 0.01*portfolio_dict[portfolio][symbol]['trade_capital']*param['account_capital']
        position = math.floor(trade_cap/security['entryprice'])
        security['position'] = position
    
        #security['stoplossprice'] = candle['maxima1Price']
        
        comment = 'SHORT strategy Entry: '+str(security['entryprice'])
        if param['show_detail_log']: print(str(candle['datetime'])+'\t'+comment)
        candle['comment']+=comment
        signal = {'datetime':candle['datetime'],'Short':True, 'ShortPrice':security['entryprice'],\
                  'position':security['position'],'comment':comment,'SMA1':candle['SMA1'],'SMA10':candle['SMA10'],\
                 'SMA15':candle['SMA15'],'EMA15':candle['EMA15'],'momentum':candle['momentum'],\
                  'momentumPrev':candles[index-1]['momentum'],'momentumSMA':candle['momentumSMA'],\
                  'momentumPrevSMA':candles[index-1]['momentumSMA']}
        security['signal'].append(signal)
        
        
    if security['trade_in']<0 and candles[index][cover]:
        candle[portfolio+'trade']=0
        security['trade_in'] = 0
        security['exitprice'] = candle['close']
        security['position'] = 0
        
        comment = 'SHORT strategy Exit: '+str(security['exitprice'])
        if param['show_detail_log']: print(str(candle['datetime'])+'\t'+comment)
        candle['comment']+=comment
        signal = {'datetime':candle['datetime'],'CloseShort':True, 'CloseShortPrice':security['exitprice'],\
                  'position':security['position'],'comment':comment}
        security['signal'].append(signal)
    elif security['trade_in']<0 and TPExit:
        candle[portfolio+'trade']=0
        security['trade_in'] = 0
        security['exitprice'] = candle['close']
        security['position'] = 0
        
        comment = 'SHORT TargetProfit Exit: '+str(security['exitprice'])
        if param['show_detail_log']: print(str(candle['datetime'])+'\t'+comment)
        candle['comment']+=comment
        signal = {'datetime':candle['datetime'],'CloseShort':True, 'CloseShortPrice':security['exitprice'],\
                  'position':security['position'],'comment':comment}
        security['signal'].append(signal)    
    elif security['trade_in']<0 and SLExit:
        candle[portfolio+'trade']=0
        security['trade_in'] = 0
        security['exitprice'] = candle['close']
        security['position'] = 0
        
        comment = 'SHORT StopLoss Exit: '+str(security['exitprice'])
        if param['show_detail_log']: print(str(candle['datetime'])+'\t'+comment)
        candle['comment']+=comment
        signal = {'datetime':candle['datetime'],'CloseShort':True, 'CloseShortPrice':security['exitprice'],\
                  'position':security['position'],'comment':comment}
        security['signal'].append(signal)
    
    
    return






import math
import numpy as np
from datetime import datetime
import pandas as pd


def check_intraday_squareoff(symbol, candles, index, portfolio_dict, portfolio, param):
    candle = candles[index]
    security =  portfolio_dict[portfolio][symbol]
   
    now=candle['datetime']
    hour = now.hour
    minute = now.minute
    clocktime = 100*hour+minute
    
    frequency = int(param['frequency'])
    nextclocktime = 100*hour+(minute+frequency)   


    tradeSquareOff = False
    tradeSquareOff = param['tradeSquare'] == True and \
    param['tradeSquareTime'] >= clocktime and param['tradeSquareTime'] <= nextclocktime
    
    tradeSquareOffPast = False
    tradeSquareOffPast = param['tradeSquare'] == True and \
    param['tradeSquareTime'] < clocktime
    
    #print(candle['datetime'],tradeSquareOff, security['trade_in'], param['tradeSquareTime'], clocktime)
    
    '-------------trade square off---------------------------'
    if tradeSquareOff and security['trade_in'] != 0:
        tmp = security['trade_in']
        security['exitprice'] = candle['open']
        security['position'] = 0
        
        if tmp>0:
            if param['show_detail_log']:print(str(candle['datetime'])+'\t'+'LONG strategy Square Exit: '+str(security['exitprice']))
            comment='LONG strategy Square Off Exit: '+str(security['exitprice'])
            candle['comment']+=comment
            signal = {'datetime':candle['datetime'],'CloseLong':True,\
                      'CloseLongPrice':security['exitprice'], 'position':security['position'],'comment':comment}
            security['signal'].append(signal)
        elif tmp<0:
            if param['show_detail_log']:print(str(candle['datetime'])+'\t'+'SHORT strategy Square Exit: '+str(security['exitprice']))
            comment='SHORT strategy Square Off Exit: '+str(security['exitprice'])
            candle['comment']+=comment
            signal = {'datetime':candle['datetime'],'CloseShort':True,\
                      'CloseShortPrice':security['exitprice'], 'position':security['position'],'comment':comment}
            security['signal'].append(signal)
        
        security['trade_in'] = 0
        
        return True
    elif tradeSquareOffPast:
        security['trade_in'] = 0
        security['exitprice'] = candle['open']
        security['position'] = 0
        return True
    
    return False




def check_tradewindow(candles, index, param):  
    now=candles[index]['datetime']
    hour = now.hour
    minute = now.minute
    clocktime = 100*hour+minute
    
    '--------------check trade window-----------------------'
    tradeWindow = True
    if param['useTradewindow'] == True:
        tradeWindow = param['tradewindowStart'] <= clocktime and param['tradewindowEnd'] >= clocktime    
    
    return tradeWindow
    

        

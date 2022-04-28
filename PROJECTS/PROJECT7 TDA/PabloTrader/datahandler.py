import pandas as pd
import pytz

from account import get_access_token
from TDAmeritrader import get_price_history_between_times




def create_candle(candle_):
    'signal data'
    '''
    candle_['green'] = 0
    candle_['red'] = 0
    candle_['breakout_long'] = 0
    candle_['breakout_short'] = 0
    candle_['minima1'] = 0
    candle_['minima2'] = 0
    candle_['minima3'] = 0
    candle_['minima1Price'] = 0.0
    candle_['minima2Price'] = 0.0
    candle_['minima3Price'] = 0.0
    candle_['maxima1'] = 0
    candle_['maxima2'] = 0
    candle_['maxima3'] = 0
    candle_['maxima1Price'] = 0.0
    candle_['maxima2Price'] = 0.0
    candle_['maxima3Price'] = 0.0
    candle_['psar'] = 0.0
    candle_['psarbull'] = -1
    candle_['hp'] = 0.0
    candle_['lp'] = 0.0
    candle_['af'] = 0.0
    candle_['volatility'] = 0.0
    candle_['SMA'] = 0.0
    candle_['EMA'] = 0.0
    candle_['RSI'] = 0.0
    
    candle_['mu'] = 0.0
    candle_['sigma'] = 0.0
    candle_['z_score'] = 0.0
    candle_['mu2'] = 0.0

    candle_['dailyReturn'] = 0.0
    candle_['histVolatility'] = 0.0
    candle_['volatilitySwitch'] = False
    '''
    
    'trade data'
    '''
    candle_['trade_in'] = 0.0
    candle_['trade_buy_close'] = 0.0
    candle_['trade_sell_close'] = 0.0
    
    candle_['buy'] = 0
    candle_['buyPrice'] = 0
    candle_['sell'] = 0
    candle_['sellPrice'] = 0
    candle_['short'] = 0
    candle_['shortPrice'] = 0
    candle_['cover'] = 0
    candle_['coverPrice'] = 0
    
    candle_['PnL'] = 0.0
    candle_['tradeprice'] = 0.0
    candle_['total_trades'] = 0.0
    candle_['long_trades'] = 0.0
    candle_['short_trades'] = 0.0
    candle_['PnL_long_trades'] = 0.0
    candle_['PnL_short_trades'] = 0.0
    candle_['cum_PnL_long_trades'] = 0.0
    candle_['cum_PnL_short_trades'] = 0.0
    candle_['sum_PnL_long_trades'] = 0.0
    candle_['sum_PnL_short_trades'] = 0.0
    candle_['net_PnL_long_trades'] = 0.0
    candle_['net_PnL_short_trades'] = 0.0
    candle_['profit_long_trades'] = 0
    candle_['profit_short_trades'] = 0
    candle_['SL_hit'] = 0
    
    candle_['trade_signal'] = 0
    candle_['trade_signal_type'] = ''
    candle_['net_PnL'] = 0.0
    candle_['trade_PnL'] = 0.0
    
    candle_['option'] = None
    candle_['optionPrice']=0.0
    candle_['optionEntryPrice']=0.0
    candle_['optionExitPrice']=0.0
    candle_['optionPnL']=0.0
    candle_['exit_flag']= 0
    candle_['exit_signal']= 0
    '''
    
    candle_['intradecount'] = 0
    candle_['comment'] = ''
    return candle_


def create_portfolio(param):
    for symbol in param['instrument_symbol_list']:
        pass

    


def get_backdata(param):
    instrument_symbol_list = param['instrument_symbol_list']
    timeframe = param['timeframe']
    
    frequency = param['frequency']# if param['multiframe']==False else tf
    #if frequency==None:
    #    return None, None
    
    extended_hours = param['extended_hours']
    periodType = param['periodType']
    period = param['period']
    
    
    sam = '1min'
    if frequency=='5':
        sam='5min'
    if frequency=='10':
        sam='10min'    
    if frequency=='15':
        sam='15min'
    if frequency=='30':
        sam='30min'
    if frequency=='60':
        sam='60min'
    if frequency=='240':
        sam='240min'    
    
    mult = '1min'
    if frequency == '60':
        frequency = '30'
        mult = '60min'
    if frequency == '240':
        frequency = '30'
        mult = '240min'
    
    
    if param['multiframe'] == True:
        frequency = '15'
    
    
    if param['data_source'] == 'offline':
        historyData_dict = {}
        for symbol in instrument_symbol_list:
            try:    
                filename = symbol+'_RAW.csv'
                filepath = './data/'+filename
                df = pd.read_csv(filepath,usecols=['datetime','close','open','high','low','volume'])
                #print(df.dtypes)
                df['datetime'] = pd.to_datetime(df['datetime'])
                #print(df.dtypes)
                historyData_dict[symbol] = df.to_dict('records')
                print(symbol+' offline backdata interval:')
                print(historyData_dict[symbol][0])
                print(historyData_dict[symbol][-1])
            except:
                print('offline data read failed for:',symbol)
        return historyData_dict
        
    try:
        ACCESS_TOKEN = get_access_token()
        #print(ACCESS_TOKEN)
    except:
        print('backdata access token generation failed, exiting')
        print('check your internet connection')
        return None

    historyData_dict = {}
    history15Data_dict = {}
    history30Data_dict = {}
    history60Data_dict = {}
    history240Data_dict = {}
    for symbol in instrument_symbol_list:
        if True:    
            dfp = None
            df = None
            df15 = None
            df30 = None
            df60 = None
            df240 = None
            #df = get_price_history(symbol=symbol, periodType=periodType,period=period,
            #                                    frequencyType=timeframe, frequency=frequency,
            #                                    needExtendedHoursData=extended_hours, access_token=ACCESS_TOKEN)
            df = get_price_history_between_times(symbol, periodType, period, timeframe, frequency,extended_hours, ACCESS_TOKEN)
            
            dfp = df.copy()
            
            if param['multiframe']==True:
                df30 = get_price_history_between_times(symbol, periodType, period, timeframe, '30',extended_hours, ACCESS_TOKEN)
                df = df30.copy()
            
            #print("df30 IN",df30.head(10))
            #print(df.tail(10))
            #print(df.last(1))
           
            if mult=='60min' or param['multiframe']==True:
                for i in range(len(df)):
                    if i%2==1: df.loc[i,'open'] = df.loc[i,'open']
                    
                    if i%2==0 and i<len(df)-1: df.loc[i,'close'] = df.loc[i+1,'close']    
                    
                    if i%2==0 and i<len(df)-1: df.loc[i,'low'] = min(df.loc[i,'low'], df.loc[i+1,'low'])
                    if i%2==1: df.loc[i,'low'] = min(df.loc[i,'low'], df.loc[i-1,'low'])    
                        
                    if i%2==0 and i<len(df)-1: df.loc[i,'high'] = max(df.loc[i,'high'], df.loc[i+1,'high'])
                    if i%2==1: df.loc[i,'low'] = max(df.loc[i,'high'], df.loc[i-1,'high'])  
                        
                    #if i%2==0 and i<len(df)-1: df.loc[i,'volume'] = sum(df.loc[i,'high'], df.loc[i+1,'high'])
                    #if i%2==1: df.loc[i,'low'] = sum(df.loc[i,'high'], df.loc[i-1,'high'])    
                    
                df = df.set_index('datetime')
                df = df.resample('60min').fillna(method = 'ffill')
                df = df.reset_index()
                
                #df = df.append(df.tail(1))
                #df.index[-1] = df.index[-2]
                #dr= df
                
                #df = df.groupby(pd.Grouper(freq='1H')).agg({'low': lambda s: s.min(), 
                #                         'high': lambda s: s.max(),
                #                         'open': lambda s: s[0],
                #                         'close': lambda s: s[-1],
                #                         'volume': lambda s: s.sum()})
                #df = df.reset_index()
            if param['multiframe']==True:
                df60 = df.copy()
            
            #print("df60 reset",df60.head())
            
            
            if param['multiframe']==True:
                df = df30.copy()
            
            if mult=='240min' or param['multiframe']==True:
                df = df.set_index('datetime')
                df = df.resample('240min').fillna(method = 'ffill')
                df = df.reset_index()
            
            if param['multiframe']==True:
                df240 = df.copy()
            
            
            
            if timeframe=='daily':
                df15 = get_price_history_between_times(symbol, periodType, period, timeframe, '1', extended_hours, ACCESS_TOKEN)
            else:        
                df15 = get_price_history_between_times(symbol, periodType, period, timeframe, '15', extended_hours, ACCESS_TOKEN)
                #df30 = get_price_history_between_times(symbol, periodType, period, timeframe, '15', extended_hours, ACCESS_TOKEN)
                
                '''
                df15 = df15.set_index('datetime')

                df15 = df15.resample(sam).fillna(method = 'ffill')
                df15 = df15.reset_index()

                cond  = ~df15['datetime'].isin(df['datetime'])
                df15.drop(df15[cond].index, inplace = True)

                cond2  = ~df['datetime'].isin(df15['datetime'])
                df15 = df15.append(df[cond2])

                df15 = df15.reset_index()
                '''
                
                
            df = dfp.copy()    
            
            
            df['index15'] = ''
            df15['index15'] = ''
            df15.index15 = df15.index
            df15 = df15.set_index('datetime')
            
            if param['multiframe']==True:
                df['index30'] = ''
                df30['index30'] = ''
                df30.index30 = df30.index
                df30 = df30.set_index('datetime')

                df['index60'] = ''
                df60['index60'] = ''
                df60.index60 = df60.index
                df60 = df60.set_index('datetime')

                df['index240'] = ''
                df240['index240'] = ''
                df240.index240 = df240.index
                df240 = df240.set_index('datetime')
            
            
            #print(df.head(2))
            #print(df15.head(2))
            
            
            for i in range(len(df)):
                dt = df.loc[i,'datetime']
                
                il = df15.index.get_loc(dt, method='pad')
                df.loc[i,'index15'] = df15.index15[il]
                
            if param['multiframe']==True:
                for i in range(len(df)):
                    dt = df.loc[i,'datetime']
                    
                    i30 = df30.index.get_loc(dt, method='pad')
                    df.loc[i,'index30'] = df30.index30[i30]

                    i60 = df60.index.get_loc(dt, method='pad')
                    df.loc[i,'index60'] = df60.index60[i60]

                    i240 = df240.index.get_loc(dt, method='pad')
                    df.loc[i,'index240'] = df240.index240[i240]
            
            
            if False:
                print("df head: ",df.head(10))
                print("df tail: ",df.tail(10))
                if param['multiframe']==True:
                    print("df240 resample head: ",df240.head(10))
                    print("df240 resample tail: ",df240.tail(10))
            
            
            #print("df15 resample head: ",df15.head(10))
            
            #df = get_price_history_recent(symbol=symbol,period=60,
            #                                    frequencyType=timeframe, frequency=frequency,
            #                                    needExtendedHoursData=extended_hours, access_token=ACCESS_TOKEN)
            
            print("dfcount",len(df))
            print("df15count",len(df15))
            
            if param['multiframe']==True:
                print("df30count",len(df30))
                print("df60count",len(df60))
                print("df240count",len(df240))
            
            historyData_dict[symbol] = df.to_dict('records')
            
            history15Data_dict[symbol] = df15.to_dict('records')
            
            if param['multiframe']==True:
                history30Data_dict[symbol] = df30.to_dict('records')
                history60Data_dict[symbol] = df60.to_dict('records')
                history240Data_dict[symbol] = df240.to_dict('records')
                
            
            print(symbol+' backdata interval:')
            print(historyData_dict[symbol][0])
            print(historyData_dict[symbol][-1])
        else:
            print('backdata fetch failed for ', symbol)
            print('exiting trading system, please try again')
            return None
            
    return historyData_dict, history15Data_dict, history30Data_dict, history60Data_dict, history240Data_dict




def update_candles(new_now=None, hisD=None, candles=None, append=False, useoffset=False):        
    now_ = new_now
    tz = pytz.timezone('US/Eastern')
    now=now_.astimezone(tz)
    
    minute=now.minute
    
    last_date = hisD[-1]['datetime']
    
    #print(last_date,  type(last_date))
    
    last_date_minute = last_date.minute
    
    #print(now, last_date)
    #print(minute, last_date_minute)
    
    offset=1
    #if useoffset and minute==last_date_minute:
    #    offset=2
    
    #global g_tick
    #if append is True:
    c = hisD[-offset]
    #else:
    # c=hisD[-1]
    dtnow = hisD[-1]['datetime']
    dtnow = dtnow.replace(year=now.year)
    dtnow = dtnow.replace(month=now.month)
    dtnow = dtnow.replace(day=now.day)
    dtnow = dtnow.replace(hour=now.hour)
    dtnow = dtnow.replace(minute=now.minute)
    if append is True:
        dt = dtnow
    else:
        dt = candles[-1]['datetime']
    
    
    new_data = {'datetime': dt,
     'open': c['open'],
     'high': c['high'],
     'low': c['low'],
     'close': c['close'],
     'volume': c['volume']}

    #print(new_data)

    #print(str(new_data['date']))

    new_candle = candles[-1].copy()
    
    if append is True:
        new_candle = create_candle(new_candle)
        
    new_candle['datetime'] = new_data['datetime']
    new_candle['open'] = new_data['open']
    new_candle['high'] = new_data['high']
    new_candle['low'] = new_data['low']
    new_candle['close'] = new_data['close']
    new_candle['volume'] = new_data['volume']

    #print(new_candle)
    candle_exist  = candles[-1]['datetime'].minute==new_candle['datetime'].minute
    
    if append is True and (not candle_exist):
        candles.append(new_candle)
    else:
        candles[-1] = new_candle
    
    newbar = minute==last_date_minute
    
    
    # consolidate old candle
    #if append is True:
    #    old_i = 2 if newbar else 1
    #    candles[-2]['open'] = hisD[-old_i]['open']
    #    candles[-2]['high'] = hisD[-old_i]['high']
    #    candles[-2]['low'] = hisD[-old_i]['low']
    #    candles[-2]['close'] = hisD[-old_i]['close']
    #    candles[-2]['volume'] = hisD[-old_i]['volume']
    
    
    return candles, newbar







def mean_reversion_strategy(df, candles, index, param, portfolio):
    if 'mean_reversion_period' not in param.keys():
        print('mean_reversion_period parameter missing')
        return
    
    if 'mean_reversion_secondary_period' not in param.keys():
        print('mean_reversion_secondary_period parameter missing')
        return
    
    if 'z_entry' not in param.keys():
        print('z_entry parameter missing')
        return
    
    if 'z_exit' not in param.keys():
        print('z_exit parameter missing')
        return 
    
    
    candle = candles[index]
    
    
    '''-----------------------------Signal calculations-----------------------'''    
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

    if index<2:
        return candle
    
    candle_p1 = candles[index-1]
    candle_p2 = candles[index-2]
    
    #print(candle_prev, index)
    
    p = param['mean_reversion_period']
    p_s = param['mean_reversion_secondary_period']
    
    
    x = candle['close']
    close = df['close'].iloc[max(0,index-p+1):index+1]
    mu = close.mean()
    #print(mu)
    candle['mu'] = mu
    
    sigma = close.std()
    #print(sigma)
    candle['sigma'] = sigma
    
    z = (x-mu)/sigma
    #print(z)
    candle['z_score']  = z
    
    
    close_s = df['close'].iloc[max(0,index-p_s+1):index+1]
    mu_s = close_s.mean()
    candle['mu2'] = mu_s
    
    
    if ( candle_p1['z_score']<-param['z_entry'] and candle_p2['z_score']>-param['z_entry'] ) and candle_p1['mu']>candle_p1['mu2']:
        candle[buy] = True
   
    if candle_p1['z_score']>-param['z_exit'] and candle_p2['z_score']<-param['z_exit']:
        candle[sell] = True
        candle[sellPrice] = candle['open'] 
    
    
    
    
    if ( candle_p1['z_score']>param['z_entry'] and candle_p2['z_score']<param['z_entry'] ) and candle_p1['mu']<candle_p1['mu2']:
        candle['short'] = True
    
    if candle_p1['z_score']<param['z_exit'] and candle_p2['z_score']>param['z_exit']:
        candle[cover] = True
        candle[coverPrice] = candle['open']
    
    return candle
        
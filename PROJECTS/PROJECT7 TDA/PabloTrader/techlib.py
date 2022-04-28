import math
import numpy as np
import pandas as pd
from datetime import date
import statistics

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__



def LogReturns(M=None):
    return np.log(M / M.shift(1))


def SMA(M=None, period=20):
    sma = M.rolling(period,min_periods=1).mean().rename("Simple Moving Average("+str(period)+")")
    return sma


def SMACandle(S, index, period):
    if index<period-1:
        return S.values[-1]
        
    arr = np.array(S)
    sum_=0.0
    for i in range(period):
        sum_ = sum_ + arr[index+i+1-period]
    return sum_/period


def SMACandleKey(candles, index, period, key):
    if index<period-1:
        return candles[index][key]
    
    
    #print("SMAM",index, period)
    #print(len(candles))
    
    #arr = np.array(S)
    sum_=0.0
    #period = min(period,index)
    try:
        for i in range(period):
            sum_ = sum_ + candles[index+i+1-period][key]
    except:
        print(index, period, len(candles), key, candles[-1])
    return sum_/period


def EMA(M=None, period=20):
    return M.ewm(span=period).mean().rename("Exponential Moving Average("+str(period)+")")    


def EMACandle(S, index, period):
    if index<period-1:
        return S.values[-1]
    
    fac = 2.0/(period+1)
    
    arr = np.array(S)
    
    ema = fac*arr[index] + (1-fac)*arr[index-1]
    
    return ema


    
def EMACandleKey(candles, index, period, key):
    if index<period-1:
        return candles[index][key]
    
    fac = 2.0/(period+1)
    
    #arr = np.array(S)
    
    candles[index]['EMA'] = fac*candles[index][key] + (1-fac)*candles[index-1]['EMA']
    
    return candles[index]['EMA']


def EMAKeyCandleKey(candles, index, period, key, emakey):
    if index<period-1:
        return candles[index][key]
    
    fac = 2.0/(period+1)
    
    #arr = np.array(S)
    
    candles[index][emakey] = fac*candles[index][key] + (1-fac)*candles[index-1][emakey]
    
    return candles[index][emakey]



def RSI(M=None, period=14):
    delta = M.diff()
    delta.iloc[0] = 0
    #print("delta shape=",delta.shape)
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up = up.ewm(span=period).mean()
    roll_down = down.abs().ewm(span=period).mean()
    RS = roll_up / roll_down
    RSI = 100.0 - (100.0 / (1.0 + RS))
    return RSI.rename("Relative Strength Index("+str(period)+")")


def Volatility(M=None):
    log_ret = np.log(M / M.shift(1))
    #log_ret = self.C.pct_change()
    vol = log_ret.rolling(252).std() * np.sqrt(252)
    return vol.rename("Annualized Volatility")


def ADX(H=None, L=None, C=None, period = 14):
    UpMove = H - H.shift(1)
    DoMove = L.shift(1) - L
    UpD = pd.Series(UpMove)
    DoD = pd.Series(DoMove)
    UpD[(UpMove<=DoMove)|(UpMove <= 0)] = 0
    DoD[(DoMove<=UpMove)|(DoMove <= 0)] = 0
    hll = H-L
    hlpc = abs(H-C.shift(1))
    llpc = abs(L-C.shift(1))
    tr = np.maximum(hll , hlpc)
    tr = np.maximum(tr , llpc)            
    ATR = tr.rolling(period).mean()       
    PosDI = (UpD.ewm(span = period).mean()).divide(ATR)
    NegDI = (DoD.ewm(span = period).mean()).divide(ATR)
    DX = 100 * (PosDI - NegDI) / (PosDI + NegDI) 
    DX = abs(DX)
    ADX = DX.ewm(span = period).mean().rename("ATR("+str(period)+")")
    return ADX


def BollingerBand(M=None, period=20):
    middle_band = M.rolling(period,min_periods=1).mean().rename("Bolliner Middle Band("+str(period)+")")
    std =  M.rolling(min_periods=period, window=period, center=False).std()
    upper_band = (middle_band + (std * 2)).rename("Bolliner Upper Band("+str(period)+")")
    lower_band = (middle_band - (std * 2)).rename("Bolliner Lower Band("+str(period)+")")
    return middle_band, upper_band, lower_band


def MACD(M=None, periodEMA1=26, periodEMA2=12, periodSignal=9):
    ema1 = M.ewm(span=periodEMA1).mean()
    ema2 = M.ewm(span=periodEMA2).mean()
    MACD = ema1 - ema2
    Signal = MACD.ewm(span=periodSignal).mean()
    return MACD.rename("MACD"),Signal.rename("Signal")


def Ichimoku(data=None, tenkan=9, kijun=26, senkou=52, senkou_lead=26, chikou=26):
    if data is None: return None
    hi_tenkan = data.high.rolling(tenkan,min_periods=1).max()
    lo_tenkan = data.low.rolling(tenkan,min_periods=1).min()
    tenkan_sen = (hi_tenkan + lo_tenkan) / 2.0
    
    hi_kijun = data.high.rolling(kijun,min_periods=1).max()
    lo_kijun = data.low.rolling(kijun,min_periods=1).min()
    kijun_sen = (hi_kijun + lo_kijun) / 2.0
    
    senkou_span_a_pre = (tenkan_sen + kijun_sen) / 2.0
    senkou_span_a = senkou_span_a_pre.shift(senkou_lead)

    hi_senkou = data.high.rolling(senkou,min_periods=1).max()
    lo_senkou = data.low.rolling(senkou,min_periods=1).min()
    senkou_span_b_pre = (hi_senkou + lo_senkou) / 2.0
        
    senkou_span_b = senkou_span_b_pre.shift(senkou_lead)

    chikou_span = data.close.shift(-chikou)
    return tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span

def PSAR(barsdata, iaf = 0.02, maxaf = 0.2):
    length = len(barsdata)
    price = barsdata['close']
    
    high = list(barsdata['high'])
    low = list(barsdata['low'])
    close = list(barsdata['close'])
    
    
    psar = close[0:len(close)]
    psarbull = [None] * length
    psarbear = [None] * length
    bull = True
    af = iaf
    ep = low[0]
    hp = high[0]
    lp = low[0]
    for i in range(2,length):
        if bull:
            psar[i] = psar[i - 1] + af * (hp - psar[i - 1])
        else:
            psar[i] = psar[i - 1] + af * (lp - psar[i - 1])
        reverse = False
        if bull:
            if low[i] < psar[i]:
                bull = False
                reverse = True
                psar[i] = hp
                lp = low[i]
                af = iaf
        else:
            if high[i] > psar[i]:
                bull = True
                reverse = True
                psar[i] = lp
                hp = high[i]
                af = iaf
        if not reverse:
            if bull:
                if high[i] > hp:
                    hp = high[i]
                    af = min(af + iaf, maxaf)
                if low[i - 1] < psar[i]:
                    psar[i] = low[i - 1]
                if low[i - 2] < psar[i]:
                    psar[i] = low[i - 2]
            else:
                if low[i] < lp:
                    lp = low[i]
                    af = min(af + iaf, maxaf)
                if high[i - 1] > psar[i]:
                    psar[i] = high[i - 1]
                if high[i - 2] > psar[i]:
                    psar[i] = high[i - 2]
        if bull:
            psarbull[i] = psar[i]
        else:
            psarbear[i] = psar[i]
    a = pd.Series(psar, index=price.index)
    b = pd.Series(psarbear, index=price.index)
    c = pd.Series(psarbull, index=price.index)
    return a, b, c



def ATR(high, low, close, n=14, fillna=False, averageType='simple'):
    """Average True Range (ATR)
    The indicator provide an indication of the degree of price volatility.
    Strong moves, in either direction, are often accompanied by large ranges,
    or large True Ranges.
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_true_range_atr
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        n(int): n period.
    Returns:
        pandas.Series: New feature generated.
    """
    cs = close.shift(1)
    TR = high.combine(cs, max) - low.combine(cs, min)
    
    
    
    '''
    ATR = np.zeros(len(close))
    atr[0] = tr[1::].mean()
    for i in range(1, len(atr)):
        atr[i] = (atr[i-1] * (n-1) + tr.iloc[i]) / float(n)

    atr = pd.Series(data=atr, index=tr.index)
    '''
    
    ATRPeriod = n
    if averageType=='wilders':
        ATR = TR.ewm(alpha=1/ATRPeriod).mean()
    elif averageType=='simple':
        ATR = TR.rolling(ATRPeriod).mean()
    else:
        ATR = TR.ewm(span=ATRPeriod).mean()
    
    
    if fillna:
        ATR = ATR.replace([np.inf, -np.inf], np.nan).fillna(0)

    return pd.Series(ATR, name='atr')




def KeltnerChannel(barsdata=None, period=20, factor=1.5):
    high = barsdata['high']
    low = barsdata['low']
    close = barsdata['close']
    
    atr =  ATR(high, low, close, n=period, fillna=False)
        
    middle_band = close.rolling(period,min_periods=1).mean().rename("Keltner Middle Band("+str(period)+")")
    upper_band = (middle_band + (atr * factor)).rename("Keltner Upper Band("+str(period)+")")
    lower_band = (middle_band - (atr * factor)).rename("Keltner Lower Band("+str(period)+")")
    
    return middle_band, upper_band, lower_band

def KAMA(price, effRatioLength=10, fastLength=2, slowLength=30):
    #input price = close;
    #input fastLength = 2;
    #input slowLength = 30;
    #input effRatioLength = 10;
    ''' kama indicator '''    
    ''' accepts pandas dataframe of prices '''
    n = effRatioLength
    pow1 = fastLength
    pow2 = slowLength
    
    

    ER_num = abs( price - price.shift(n) )
    
    absDiffx = abs(price - price.shift(1) )  
    ER_den = absDiffx.rolling(n).sum()
    
    ER = ER_num / ER_den

    sc = ( ER*(2.0/(pow1+1)-2.0/(pow2+1.0))+2/(pow2+1.0) ) ** 2.0


    answer = np.zeros(sc.size)
    N = len(answer)
    first_value = True

    for i in range(N):
        if sc[i] != sc[i]:
            answer[i] = np.nan
        else:
            if first_value:
                answer[i] = price[i]
                first_value = False
            else:
                answer[i] = answer[i-1] + sc[i] * (price[i] - answer[i-1])
    return pd.Series(answer, index=price.index)



def ATRTrailingStop(df, ATRPeriod=5, ATRFactor=3.5, trailType="modified", firstTrade='long', averageType='wilders'):
    C = df['close']
    H = df['high']
    L = df['low']
    
    
    if trailType=="modified":
        HiLoref = 1.5*(H-L).rolling(ATRPeriod).sum()
        HiminusLo = H-L 
        HiLo = HiminusLo.combine(HiLoref, min)
    
        HRefpre = np.where( L<=H.shift(1), H-C.shift(1), (H - C.shift(1)) - 0.5 * (L - H.shift(1)) )
        HRef = pd.Series(HRefpre, index=C.index)
    
        LRefpre =np.where( H>=L.shift(1), C.shift(1)-L, (C.shift(1) - L) - 0.5 * (L.shift(1) - H) )
        LRef = pd.Series(LRefpre, index=C.index)
    
        TRpre = HRef.combine(LRef,max)
        TR = TRpre.combine(HiLo, max)
    else:
        CS = C.shift(1)
        TR = H.combine(CS, max) - L.combine(CS, min)
    
    
    if averageType=='wilders':
        ATR = TR.ewm(alpha=1/ATRPeriod).mean()
    elif averageType=='simple':
        ATR = TR.rolling(ATRPeriod).mean()
    else:
        ATR = TR.ewm(span=ATRPeriod).mean()
    
    loss = ATRFactor * ATR
    
    Clist = list(C)
    losslist = list(loss)
    statelist = [1]*len(df)
    traillist = [0]*len(df)
    
    for i in range(len(df)):
        if i==0:
            statelist[i] = 0
            traillist[i] = float('nan')
            continue        
        
        if statelist[i-1] == 0 and math.isnan(losslist[i]):
            statelist[i] = 0
            traillist[i] = float('nan')            
            
        if statelist[i-1] == 0 and not math.isnan(losslist[i]):
            statelist[i] = 1
            traillist[i] = Clist[i] - losslist[i]
            
        
        if statelist[i-1] == 1 and Clist[i] > traillist[i-1]:
            statelist[i] = 1
            traillist[i] = max(traillist[i-1], Clist[i] - losslist[i])
        
        elif statelist[i-1] == 1 and Clist[i] <= traillist[i-1]:
            statelist[i] = -1
            traillist[i] = Clist[i] + losslist[i]
        
        elif statelist[i-1] == -1 and Clist[i] < traillist[i-1]:
            statelist[i] = -1
            traillist[i] = min(traillist[i-1], Clist[i] + losslist[i])
        
        elif statelist[i-1] == -1 and Clist[i] >= traillist[i-1]:
            statelist[i] = 1
            traillist[i] = Clist[i] - losslist[i]
    
    return pd.Series(traillist, index=C.index)
                



def WMA(C=None, Period=200):
    def f(N):
        w =  np.arange(1,N+1)
        def g(x):
            return (w*x).sum() / w.sum()
        return g
    return C.rolling(window=Period).apply(f(Period))



def WMACandleKey(candles, index, Period, key):
    if index<Period-1:
        return candles[index][key]
    
    w =  np.arange(1,Period+1)
    wsum = w.sum()
    sum_=0.0
    for i in range(Period):
        sum_ +=  w[i]*candles[index+i+1-Period][key] 
    wma = sum_/wsum
    return wma

def HullMACandleKey(candles, index, Period, key):
    #if index<Period-1:    
    #    return candles[index][key]
    
    candle = candles[index]
    candle['wma'+str(Period)] = WMACandleKey(candles, index, Period, key)
    candle['wma'+str(Period)+'bytwo'] = WMACandleKey(candles, index, int(Period/2), key)
    candle['hullpre'+str(Period)] = 2*candle['wma'+str(Period)+'bytwo'] - candle['wma'+str(Period)]
    candle['hullMA'+str(Period)] = WMACandleKey(candles, index, int(math.sqrt(Period)), 'hullpre'+str(Period))
    return candle['hullMA'+str(Period)]
    #return WMA(2*WMA(C, int(Period/2)) - WMA(C, Period), int(math.sqrt(Period)))


def HullMA(C = None, Period=200):
    return WMA(2*WMA(C, int(Period/2)) - WMA(C, Period), int(math.sqrt(Period)))


'''
def HullMACandle(C, index, period):
    def ma(C, N):
        w =  np.arange(1,N+1)
        return (w*C).sum() / w.sum()
    return ma(2*ma(S, int(period/2)) - ma(S, period), int(math.sqrt(period)))
'''




'''dictionary based calculations of volatility'''
def calc_volatility(candles=None, i=0):
    if i<252: return 0.0
    summ = 0.0
    for k in range(i-251,i+1):
        c0 = candles[k]['close']
        c1 = candles[k-1]['close']
        try:
            log_ret = np.log(c0) - np.log(c1)
        except:
            log_ret=0.0
        summ = summ+log_ret
    avg = summ/252    
    
    summ2=0.0
    for k in range(i-251,i+1):
        c0 = candles[k]['close']
        c1 = candles[k-1]['close']
        try:
            log_ret = np.log(c0) - np.log(c1)
        except:
            log_ret=0.0
        summ2 = (log_ret-avg)*(log_ret-avg)
    std_ = summ2/252 
    std = np.sqrt(std_) * np.sqrt(252)
    return std


'''dictionary based calculations of psar'''
def calc_psar(candles=None, i=0, iaf = 0.02, maxaf = 0.2):
    target = candles[i]
    
    if i<2:
        target['psar'] = target['close']
        target['psarbull'] = 1
        target['hp'] = target['high']
        target['low'] = target['low']
        target['af'] = iaf
        return
    
    previous = candles[i-1]
    p2 = candles[i-2] 
    
    af = previous['af']
    bull = previous['psarbull']
    hp = previous['hp']
    lp = previous['lp']
    
    if bull==1:
        target['psar'] = previous['psar'] + af * (hp - previous['psar'])
    else:
        target['psar'] = previous['psar'] + af * (lp - previous['psar'])
    
    reverse = False
    
    if bull==1:
        if target['low'] < target['psar']:
            target['psarbull'] = 0
            reverse = True
            target['psar'] = hp
            target['lp'] = target['low']
            target['hp'] = previous['hp']
            target['af'] = iaf
    else:
        if target['high'] > target['psar']:
            target['psarbull'] = 1
            reverse = True
            target['psar'] = lp
            target['hp'] = target['high']
            target['lp'] = previous['lp']
            target['af'] = iaf
    
    if not reverse:
        if bull==1:
            if target['high'] > hp:
                target['hp'] = target['high']
                target['af'] = min(af + iaf, maxaf)
            if previous['low'] < target['psar']:
                target['psar'] = previous['low']
            if p2['low'] < target['psar']:
                target['psar'] = p2['low']
        else:
            if target['low'] < lp:
                target['lp'] = target['low']
                target['af'] = min(af + iaf, maxaf)
            if previous['high'] > target['psar']:
                target['psar'] = previous['high']
            if p2['high'] > target['psar']:
                target['psar'] = p2['high']
    
    if target['hp']==0: target['hp'] = previous['hp']
    if target['lp']==0: target['lp'] = previous['lp']
    if target['af']==0: target['af'] = previous['af']    
    if target['psar']==0: target['psar'] = previous['psar']
    if target['psarbull']==-1: target['psarbull'] = previous['psarbull']   
    
    return





def stochfull(df=None, kperiod=14, index=0):
    if index+1<kperiod: return 0
    size = index+1
    
    array_close = np.array(df['close'])
    array_high = np.array(df['high'])
    array_low = np.array(df['low'])
    
    kmax=array_high[size-kperiod]
    for x in range(size-kperiod,size):
        kmax=max(kmax,array_high[x])
    
    kmin=array_low[size-kperiod]
    for x in range(size-kperiod,size):
        kmin=min(kmin,array_low[x])    
    
    c1 = array_close[size-1] - kmin
    c2 = kmax - kmin
    K = c1 / c2 * 100 if c2 != 0 else 0
    return K



def vwapweek(candles, index):
    candle = candles[index]
    
    if index < 1:
        candle['cumvolume'] = candle['volume']
        candle['vwap'] = candle['close']
        return candle['vwap']
    
    previous = candles[index-1]
    
    #print(candle['datetime'], type(candle['datetime']))
    #print(candle['datetime'].date())
    #print(candle['datetime'].date().weekday())
          
          
    w0=candle['datetime'].date().weekday()
    w1=previous['datetime'].date().weekday()
    
    if  w0 == 0 and w1==6:
        candle['cumvolume'] = candle['volume']
        candle['vwap'] = candle['close']
    else:
        candle['cumvolume'] = previous['cumvolume'] + candle['volume']
        if candle['cumvolume']==0:
            candle['vwap'] = candle['close']
        else:
            candle['vwap'] = (previous['vwap']*previous['cumvolume'] + candle['close']*candle['volume'])/candle['cumvolume']
            
    return candle['vwap']        
    
    
    
    

def getDailyData(df):
    df['openDay']=df['open']
    df['highDay']=df['high']
    df['lowDay']=df['low']
    #df['closeDay']=df['close']
    fcn = lambda x: x.date().day
    df['Date']=df['datetime'].map(fcn)
    for index, row in df.iterrows():
        if index==0:
            #df.at[index,'openDay']=row['open']
            prev=row
            continue
        if row['Date']!=prev['Date']:
            df.at[index,'openDay'] = row['open']
            df.at[index,'highDay'] = row['high']
            df.at[index,'lowDay'] = row['low']

        else:
            df.at[index,'openDay'] = prev['openDay']
            df.at[index,'highDay'] = max(prev['highDay'],row['high'])
            df.at[index,'lowDay'] = min(prev['lowDay'],row['low'])                     
        prev=df.iloc[index]                  
    return df



def getDailyDataOnCandle(candles, index):
    candle = candles[index]
    
    if index<1:
        candle['openDay'] = candle['open']
        candle['highDay'] = candle['high']
        candle['lowDay'] = candle['low']
        return
    
    #candle = candles[index]
    previous = candles[index-1]
    
    #print(candle['datetime'].date().day)
    #print(previous['datetime'].date().day)
    #print(previous['openDay'])
    
    if candle['datetime'].date().day != previous['datetime'].date().day:
        candle['openDay'] = candle['open']
        candle['highDay'] = candle['high']
        candle['lowDay'] = candle['low']
    else:
        candle['openDay'] =  previous['openDay']
        candle['highDay'] =  max(previous['highDay'], candle['high'])
        candle['lowDay'] =  min(previous['lowDay'], candle['low'])
    
    return





def stochfullCandle(candles, index, kperiod):
    if index+1<kperiod: return 0
    size = index+1
    
    #array_close = np.array(df['close'])
    #array_high = np.array(df['high'])
    #array_low = np.array(df['low'])
    
    kmax=candles[size-kperiod]['high']
    for x in range(size-kperiod,size):
        kmax=max(kmax,candles[x]['high'])
    
    kmin=candles[size-kperiod]['low']
    for x in range(size-kperiod,size):
        kmin=min(kmin,candles[x]['low'])    
    
    c1 = candles[index]['close'] - kmin
    c2 = kmax - kmin
    K = c1 / c2 * 100 if c2 != 0 else 0
    return K



def vwapweek(candles, index):
    candle = candles[index]
    
    if index < 1:
        candle['cumvolume'] = candle['volume']
        candle['vwap'] = candle['close']
        return candle['vwap']
    
    previous = candles[index-1]
    
    #print(candle['datetime'], type(candle['datetime']))
    #print(candle['datetime'].date())
    #print(candle['datetime'].date().weekday())
          
          
    w0=candle['datetime'].date().weekday()
    w1=previous['datetime'].date().weekday()
    
    #candle['w0'] = w0
    #candle['w1'] = w1
    
    if  w0 == 0 and w1!=0:
        candle['cumvolume'] = candle['volume']
        candle['vwap'] = candle['close']
    else:
        candle['cumvolume'] = previous['cumvolume'] + candle['volume']
        if candle['cumvolume']==0:
            candle['vwap'] = candle['close']
        else:
            candle['vwap'] = (previous['vwap']*previous['cumvolume'] + candle['close']*candle['volume'])/candle['cumvolume']
            
    return candle['vwap']        
    
    
    
def totalvolumeday(candles, index):
    candle = candles[index]
    
    if index < 1:
        candle['totalvolumeday'] = candle['volume']
        return candle['totalvolumeday']
    
    previous = candles[index-1]
    
    #print(candle['datetime'], type(candle['datetime']))
    #print(candle['datetime'].date())
    #print(candle['datetime'].date().weekday())
          
          
    w0=candle['datetime'].date().weekday()
    w1=previous['datetime'].date().weekday()
    
    if  w0 != w1:
        candle['totalvolumeday'] = candle['volume']
    else:
        candle['totalvolumeday'] = previous['totalvolumeday'] + candle['volume']
        
            
    return candle['totalvolumeday']        
    
    
    
    

        
def volatility_switch(candles=None, index=0, param=None, period=21):
    '''
    def dailyReturn = (price - price[1]) / ( (price + price[1]) / 2 );
    def histVolatility = StDev(dailyReturn, length);
    def VolatilitySwitch = ( fold i = 0 to length with count 
    do count + if histVolatility[i] <= histVolatility then 1 else 0 ) / length;
    '''
    candle = candles[index]
    
    p=period
    histmax = min(index+1,p)
    
    if index < 1:
        candle['dailyReturn'] = 0.0
        candle['histVolatility'] = 0.0
        candle['volatilitySwitch'] = False
        return candle['volatilitySwitch']
    
    c1 = candles[index-0]['close']
    c2 = candles[index-1]['close']
    
    try:
        dailyReturn = (c1 - c2) / ( (c1 + c2) / 2 )
    except:
        dailyReturn = 0.0
    
    candle['dailyReturn'] = dailyReturn
    
    #df['dailyReturn'].at[index] = candle['dailyReturn']
    #histVolatility = df['dailyReturn'].iloc[max(0,index-p+1):index+1].std()
    
    sample = []
    for i in range(histmax):
        sample.append(candles[index-i]['dailyReturn'])
        
    histVolatility = statistics.stdev(sample)
    candle['histVolatility'] = histVolatility
    
    
    count=0.0
    for i in range(histmax):
        count += 1.0 if candles[index-i]['histVolatility'] <= candles[index]['histVolatility'] else 0.0
    
    candle['volatilitySwitch'] = (count/p) < 0.5
    return candle['volatilitySwitch']




'''
def rma_up(candles, source, n):
    target = candles[n]
    if n != 0:
        previous = candles[n-1]
    length = 14
    if n < length:
        rma = float('nan')
    elif n==length:
        rma=0.0
        for i in range(1,length+1):
            rma = rma+max(candles[i][source]-candles[i-1][source],0)
            #print(rma)
        rma = rma/length
    elif n>length:
        rma = max(target[source]-previous[source],0)*(1/length) + (1-1/length)*previous['up']
    else:
        return target['up']
    return rma


def rma_down(candles, source, n):
    target = candles[n]
    if n != 0:
        previous = candles[n-1]
    length = 14
    if n < length:
        rma = float('nan')
    elif n==length:
        #rma = -min(target[source]-previous[source],0)
        rma=0.0
        for i in range(1,length+1):
            rma = rma-min(candles[i][source]-candles[i-1][source],0)
        rma = rma/length
    elif n>length:
        rma = -min(target[source]-previous[source],0)*(1/length) + (1-1/length)*previous['down']
    else:
        return target['down']
    return rma
'''

def RSICandle(candles, index, length):
    candle = candles[index]
    source = 'close'
    
    rmaup=0.0
    rmadn=0.0
    
    if index<length:
        for i in range(1,index+1):
            rmaup = rmaup+max(candles[i][source]-candles[i-1][source],0)
            rmadn = rmadn-min(candles[i][source]-candles[i-1][source],0)
        candle['rsiup'] = rmaup
        candle['rsidn'] = rmadn
    else:
        previous = candles[index-1]
        candle['rsiup'] = max(candle[source]-previous[source],0)*(1/length) + (1-1/length)*previous['rsiup']
        candle['rsidn'] = -min(candle[source]-previous[source],0)*(1/length) + (1-1/length)*previous['rsidn']
    
    if candle['rsidn'] == 0:
        candle['rsi'] = 100
    elif candle['rsiup'] == 0:
        candle['rsi'] = 0
    else:
        candle['rsi'] = 100-(100/(1+candle['rsiup']/candle['rsidn']))

    return candle['rsi']


def Momentum(candles, index, length):
    candle = candles[index]
    source = 'close'
    
    if index<length:
        candle['momentum'] = 0.0
    else:    
        offsetcandle =  candles[index-length]
        candle['momentum'] = candle[source] - offsetcandle[source]
    
    return candle['momentum']


def MomentumSMA(candles, index, length):
    candle = candles[index]
    source = 'close'
    
    if index<length:
        #candle['momentum'] = 0.0
        candle['momentumSMA'] = 0.0
    else:    
        offsetcandle =  candles[index-length]
        #candle['momentum'] = candle[source] - offsetcandle[source]
        sum_=0.0
        for i in range(length):
            sum_ = sum_ + candles[index-i]['momentum']
        candle['momentumSMA'] = sum_/length
            
    return candle['momentumSMA']
    

#def clPrev = close[1];
#def data = TotalSum(if clPrev != 0 then (close - clPrev) / clPrev * volume else 0);
#plot PVT = data;   
def PVT(candles, index):
    candle = candles[index]
    if index<1:
        candle['pvt'] = 0
        return candle['pvt']
    
    cl = candle['close']
    clPrev = candles[index-1]['close']
    volume = candle['volume']
    
    curpvt = ((cl - clPrev) / clPrev) * volume if clPrev!=0 else 0
    
    #if index==1: print(candles[index-1])
    
    candle['pvt'] = candles[index-1]['pvt'] + curpvt
    
    return candle['pvt']
    
    
    
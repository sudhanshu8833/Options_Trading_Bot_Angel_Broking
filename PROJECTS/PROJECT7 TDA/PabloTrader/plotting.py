import datetime
import time
from decimal import Decimal
import numpy as np
import pandas as pd
import requests
from datetime import date,timedelta
#import simplejson as json
import os
import os.path
import inspect

import matplotlib.pyplot as plt
#pip install https://github.com/matplotlib/mpl_finance/archive/master.zip
#from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import Formatter
from matplotlib.dates import bytespdate2num, num2date
import matplotlib
from matplotlib.widgets import Slider
#matplotlib.use('Qt4Agg')

#from plotly import __version__
#print (__version__) # requires version >= 1.9.0
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
        
        
def plot_backtest_charts(portfolio=None, symbol='AAPL', timeframe='minute', frequency='1', periodType='day', period='2', params=None, tradeDirection="LONG", extended_hours=False, candles_dict=None, indicator_list=None, portfolio_dict=None):
    if candles_dict is None:
        return
    
    if extended_hours==True:
        needExtendedHoursData = 'true'
    else:
        needExtendedHoursData = 'false'
    
    
    security = portfolio_dict[portfolio][symbol]
    signal = security['signal']
    dfsig = pd.DataFrame(signal)
    
    
    
    df = pd.DataFrame(candles_dict[symbol])

    #remove 0.0 close price
    df= df[df['close'] != 0.0]

    df.index = df['datetime']

    # --------Creating required data in new DataFrame OHLC----------------------------


    df['date'] = df.index

    #print(df.index)



    df["date"] = df["date"].apply(mdates.date2num)

    ohlc= df[['date', 'open', 'high', 'low','close']].copy()



    dates = ohlc['date'].copy()
    N = len(dates)
    ind = np.arange(N)  # the evenly spaced plot indices
    #fmt = "%d/%m/%y %H:%M"
    #def format_date(index, pos=None):
    #    thisind = np.clip(int(index + 0.5), 0, N - 1)
    #    return dates[thisind].strftime(fmt)        
    class MyFormatter(Formatter):
        def __init__(self, dates, fmt='%Y-%m-%d %H:%M'):
            self.dates = dates
            self.fmt = fmt

        def __call__(self, x, pos=0):
            'Return the label for time x at position pos'
            ind = int(np.round(x))
            if ind >= len(self.dates) or ind < 0:
                return ''

            return num2date(self.dates[ind]).strftime(self.fmt)

    formatter = MyFormatter(dates)        


    #--------------------plotly------------------------------------------------------

    data = []

    df['dates'] = df.index

    traceOHLC = go.Candlestick(x=df['dates'].astype(str), open=ohlc['open'], high=ohlc['high'], low=ohlc['low'], close=ohlc['close'], 
                              opacity=0.5, name='Prices')
    data.append(traceOHLC)


    chart_title = portfolio+"-"+symbol

    layout = go.Layout(
        title=chart_title,
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            #rangeselector = rangeselector,
            type='category', 
            categoryorder='category ascending',
            rangeslider = dict(
                visible = False
            )
            #tickcolor='#000'
        ),
        yaxis=dict(
            autorange=True
        )    
    )        


    color_list = ['rgba(255, 0, 0, .6)','rgba(0, 255, 0, .6)','rgba(0, 0 , 255, .6)',\
                  'rgba(255, 255, 0, .6)','rgba(255, 0, 255, .6)','rgba(0, 255, 255, .6)']


    ''' line indicators '''
    k=0
    for indicator in indicator_list:
        k=k%6
        if indicator[1]!='line':continue
        indicatorvalues = df[indicator[0]].tolist()
        #dash = indicator_style_list[k]
        trace = go.Scatter(x = df['dates'].astype(str), y = indicatorvalues, mode = 'lines', 
                               line = dict(color = color_list[k],), name = indicator[0])
        data.append(trace)
        k+=1


    ''' dash indicators'''    
    k=0
    for indicator in indicator_list:
        k=k%6

        clr = color_list[k]
        if 'takeprofit' in indicator[0]: clr = 'rgba(0, 255, 0, .6)'
        elif 'stoploss' in indicator[0]: clr = 'rgba(255, 0, 0, .6)'


        if indicator[1]!='dash':continue
        indicatorvalues = df[indicator[0]].tolist()
        #dash = indicator_style_list[k]
        trace = go.Scatter(x = df['dates'].astype(str), y = indicatorvalues, mode = 'lines', 
                               line = {'color':clr,'dash':'dash','width':1.0}, name = indicator[0])
        data.append(trace)
        k+=1



    '''momentum'''
    indicatorvalues = df['momentum'].tolist()
    trace = go.Scatter(x = df['dates'].astype(str), y = indicatorvalues, visible='legendonly', mode = 'lines', 
                           line = dict(color = 'blue',), name = 'momentum')
    data.append(trace)
    
    '''momentumSMA'''
    indicatorvalues = df['momentumSMA'].tolist()
    trace = go.Scatter(x = df['dates'].astype(str), y = indicatorvalues, visible='legendonly', mode = 'lines', 
                           line = dict(color = 'yellow',), name = 'momentumSMA')
    data.append(trace)
    
    '''rsi15min'''
    indicatorvalues = df['rsi15min'].tolist()
    trace = go.Scatter(x = df['dates'].astype(str), y = indicatorvalues, visible='legendonly', mode = 'lines', 
                           line = dict(color = 'green',), name = 'rsi15min')
    data.append(trace)
    
    
    '''rsisma15min'''
    indicatorvalues = df['rsisma15min'].tolist()
    trace = go.Scatter(x = df['dates'].astype(str), y = indicatorvalues, visible='legendonly', mode = 'lines', 
                           line = dict(color = 'red',), name = 'rsisma15min')
    data.append(trace)
    
    
    if params['multiframe']==True:
        '''SMA1-30min'''
        indicatorvalues = df['SMA1-30min'].tolist()
        trace = go.Scatter(x = df['dates'].astype(str), y = indicatorvalues, visible='legendonly', mode = 'lines', 
                           line = dict(color = 'red',), name = 'SMA1-30min')
        data.append(trace)
        
        
        
        '''SMA10-30min'''
        indicatorvalues = df['SMA10-30min'].tolist()
        trace = go.Scatter(x = df['dates'].astype(str), y = indicatorvalues, visible='legendonly', mode = 'lines', 
                           line = dict(color = 'green',), name = 'SMA10-30min')
        data.append(trace)
        
        
        '''SMA1-60min'''
        indicatorvalues = df['SMA1-60min'].tolist()
        trace = go.Scatter(x = df['dates'].astype(str), y = indicatorvalues, visible='legendonly', mode = 'lines', 
                           line = dict(color = 'red',), name = 'SMA1-60min')
        data.append(trace)
        
        
        
        '''SMA10-60min'''
        indicatorvalues = df['SMA10-60min'].tolist()
        trace = go.Scatter(x = df['dates'].astype(str), y = indicatorvalues, visible='legendonly', mode = 'lines', 
                           line = dict(color = 'green',), name = 'SMA10-60min')
        data.append(trace)
        
        
        
        '''SMA1-240min'''
        indicatorvalues = df['SMA1-240min'].tolist()
        trace = go.Scatter(x = df['dates'].astype(str), y = indicatorvalues, visible='legendonly', mode = 'lines', 
                           line = dict(color = 'red',), name = 'SMA1-240min')
        data.append(trace)
        
        
        
        '''SMA10-240min'''
        indicatorvalues = df['SMA10-240min'].tolist()
        trace = go.Scatter(x = df['dates'].astype(str), y = indicatorvalues, visible='legendonly', mode = 'lines', 
                           line = dict(color = 'green',), name = 'SMA10-240min')
        data.append(trace)
        
    
    #indicatorvalues = df['rsi'].tolist()
    #trace = go.Scatter(x = df['dates'].astype(str), y = indicatorvalues, visible='legendonly', mode = 'lines', 
    #                       line = dict(color = 'green',), name = 'rsi')
    #data.append(trace)
    
    
    # -----------------Signals--------------------------------
    arrowSize = 15

    '''
    traceLong = go.Scatter(
        x = df.loc[df['Long'] == True , 'dates'].astype(str),
        y = df.loc[df['Long'] ==True, 'LongPrice'].values.tolist(),
        text=df.loc[df['Long'] == True , portfolio+'position'].astype(str),
        textposition='top center',
        mode = 'markers+text',
        marker={'color': 'rgba(0, 255, 0, .8)', 'symbol': 'triangle-up', 'size': arrowSize},
        name = 'Long'
        )
    data.append(traceLong)
    '''
    
    if 'Long' in dfsig.columns:
        traceLong = go.Scatter(
            x = dfsig.loc[dfsig['Long'] == True , 'datetime'].astype(str),
            y = dfsig.loc[dfsig['Long'] ==True, 'LongPrice'].values.tolist(),
            text=dfsig.loc[dfsig['Long'] == True , 'position'].astype(str),
            textposition='top center',
            mode = 'markers+text',
            marker={'color': 'rgba(0, 255, 0, .8)', 'symbol': 'triangle-up', 'size': arrowSize},
            name = 'Long'
            )
        data.append(traceLong)



    if 'CloseLong' in dfsig.columns:
        traceCloseLong = go.Scatter(
            x = dfsig.loc[dfsig['CloseLong'] == True , 'datetime'].astype(str),
            y = dfsig.loc[dfsig['CloseLong'] ==True, 'CloseLongPrice'].values.tolist(),
            text=dfsig.loc[dfsig['CloseLong'] == True , 'position'].astype(str),
            textposition='top center',
            mode = 'markers+text',
            marker={'color': 'rgba(0, 0, 255, .8)', 'symbol': 'triangle-down', 'size': arrowSize},
            name = 'CloseLong'
            ) 
        data.append(traceCloseLong)


    if 'Short' in dfsig.columns:
        traceShort = go.Scatter(
            x = dfsig.loc[dfsig['Short'] == True , 'datetime'].astype(str),
            y = dfsig.loc[dfsig['Short'] ==True, 'ShortPrice'].values.tolist(),
            text=dfsig.loc[dfsig['Short'] == True , 'position'].astype(str),
            textposition='top center',
            mode = 'markers+text',
            marker={'color': 'rgba(255, 0, 0, .8)', 'symbol': 'triangle-down', 'size': arrowSize},
            name = 'Short'
            )
        data.append(traceShort)


    if 'CloseShort' in dfsig.columns:
        traceCloseShort = go.Scatter(
            x = dfsig.loc[dfsig['CloseShort'] == True , 'datetime'].astype(str),
            y = dfsig.loc[dfsig['CloseShort'] ==True, 'CloseShortPrice'].values.tolist(),
            text=dfsig.loc[dfsig['CloseShort'] == True , 'position'].astype(str),
            textposition='top center',
            mode = 'markers+text',
            marker={'color': 'rgba(0, 0, 0, .8)', 'symbol': 'triangle-up', 'size': arrowSize},
            name = 'CloseShort'
            ) 
        data.append(traceCloseShort)


    fig = go.Figure(data=data, layout=layout)        
    #fig.update_traces(textposition='top center')
    plot(fig, show_link = True, filename = './plots/'+portfolio+'-'+symbol+'.html')



    plt.show(block=False)
    return fig


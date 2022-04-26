import time
import os
import glob
import ast
#import json
import csv
import functools

import numpy as np
import pandas as pd

from IPython.display import display
from ipywidgets import widgets
from ipywidgets import interact,interactive, interact_manual, Button, Output, HBox, VBox, Layout

from threading import Thread
import asyncio

from trademanager import run_system
from plotting import plot_backtest_charts
from TDAmeritrader import get_account_detail
from TDAmeritrader import get_positions
from authentication import generate_refresh_token




MAX_PORTFOLIO = 1

param = {}
global live_param
live_param = {}

global candles_dict_chart
global portfolio_dict_chart
global indicator_dict_chart
candles_dict_chart = {}
portfolio_dict_chart = {}
indicator_dict_chart = {}

global live_portfolio_dict_chart
global live_indicator_dict_chart
global live_candles_dict_chart
live_portfolio_dict_chart = {}
live_indicator_dict_chart = {}
live_candles_dict_chart = {}    


#--------------------------Paramters-----------------------------------------------------------
style = {'description_width': 'initial'}
bw = '20%'


''' data source: online, offline '''
param['data_source'] = 'online'
def data_source_f(change):
    param['data_source'] = change.new
data_source_w=widgets.Dropdown(options=['offline','online'],value='online',\
                                  decription='Data Source', layout={'width': '10%'}, style=style)
data_source_w.observe(data_source_f, 'value')




''' available capital for trade in USD '''
param['account_capital'] = 10000.0
def account_capital_f(change):
    param['account_capital'] = change.new
account_capital_w=widgets.FloatText(value=param['account_capital'],description='Account Capital (USD)',disabled=False, layout={'width': '30%'}, style=style)
account_capital_w.observe(account_capital_f,'value')


''' 
Portfolio: ma_breakout_strategy, mean_reversion_strategy 
trade_capital: percent of account_capital
param['portfolio_dict'] = {'ma_breakout_strategy':{'AAPL':{'trade_capital':10},'AMZN':{'trade_capital':40}}, 
                           'mean_reversion_strategy':{'AAPL':{'trade_capital':10},'TSLA':{'trade_capital':10}}}
'''


param['portfolio_dict'] = {}
for i in range(MAX_PORTFOLIO):
    param['portfolio_dict']['Portfolio-'+str(i)] = {}
        

param['indicator_dict'] = {}
for i in range(MAX_PORTFOLIO):
    param['indicator_dict']['Portfolio-'+str(i)] = {}        
        
        
'''
param['portfolio_dict'] = {
                            'chori_strategy':
                            {
                                #'AAPL':{'trade_capital':10},
                                #'AMZN':{'trade_capital':40},
                                #'SPY':{'trade_capital':10},   
                            },
                            'bros24_strategy':
                            {
                                #'AAPL':{'trade_capital':10},
                                #'AMZN':{'trade_capital':40},
                                #'SPY':{'trade_capital':10},   
                            }
                          }
'''

'''
param['indicator_dict'] = {
                            'chori_strategy':
                            {
                                'AAPL':[('ChoriSMA','line'),('ChoriEMA','line'), \
                                        ('chori_strategy'+'stoplossprice','dash'),\
                                        ('chori_strategy'+'takeprofitprice','dash')],
                                'AMZN':[('ChoriSMA','line'),('ChoriEMA','line'), \
                                        ('chori_strategy'+'stoplossprice','dash'),\
                                        ('chori_strategy'+'takeprofitprice','dash')],
                                'SPY':[('ChoriSMA','line'),('ChoriEMA','line'), \
                                        ('chori_strategy'+'stoplossprice','dash'),\
                                        ('chori_strategy'+'takeprofitprice','dash')],   
                            },
                            'bros24_strategy':
                            {
                                'AAPL':[('bros24_i','line'),('bros24_i2','line'),\
                                        ('bros24_s','line'),('bros24_s2','line'),\
                                        ('bros24_strategy'+'takeprofitprice','dash'),\
                                        ('bros24_strategy'+'stoplossprice','dash')],
                                'AMZN':[('bros24_i','line'),('bros24_i2','line'),\
                                        ('bros24_s','line'),('bros24_s2','line')],
                                'SPY':[('bros24_i','line'),('bros24_i2','line'),\
                                       ('bros24_s','line'),('bros24_s2','line')],   
                            },
                           
                          }


'''



default_indicator_list = [('SMA1','line'), ('SMA10','line'), ('SMA15','line'), ('EMA15','line')]
                          #,('Portfolio-0'+'stoplossprice','dash')]





#strategy_list = ['ma_breakout_strategy','mean_reversion_strategy']
#strategy=widgets.Dropdown(options=strategy_list,value='ma_breakout_strategy',decription='Strategy', layout={'width': 'auto'})


param['trade_capital'] = 10.0
def trade_capital_f(change):
    param['trade_capital'] = change.new
trade_capital_w=widgets.FloatText(value=param['trade_capital'],description='Trade Capital(%)',\
                                  disabled=False, layout={'width': bw}, style=style)
trade_capital_w.observe(trade_capital_f,'value')

'''
def trade2_capital_f(change):
    param['trade_capital'] = change.new
trade2_capital_w=widgets.FloatText(value=10.0,description='Bros24 Trade Capital(%)',disabled=False, layout={'width': 'auto'}, style=style)
trade2_capital_w.observe(trade2_capital_f,'value')
'''


symbol_short_list = []
try:
    with open('./CUSTOM_STOCKS.csv', newline='') as csvfile:
        custom_stock_reader = csv.reader(csvfile, delimiter=',')
        for row in custom_stock_reader: symbol_short_list=symbol_short_list+row
    #print(symbol_short_list)
    for s in symbol_short_list:
        if ' ' in s:
            print('WARNING: Space found in symbol name, please correct:',s)
except:
    print('WARNING: CUSTOM_STOCKS.csv read failed, confirm if values in file are comma separated')
    symbol_short_list = ['AAPL','AMZN','MSFT','SPY','FB','NFLX']    
    


symbol_df = pd.read_csv('./SP500.csv')
symbol_list = symbol_df['Symbol'].to_list()
symbol=widgets.Dropdown(options=symbol_list,value='AAPL',decription='Symbol', layout={'width': '10%'}, style=style)





strategy_w_list = [None]*MAX_PORTFOLIO
symbols_w_list = [None]*MAX_PORTFOLIO
symbols_select_w_list = [None]*MAX_PORTFOLIO
button_symbols_reset_w_list = [None]*MAX_PORTFOLIO


def strategy_f(change, n=0):
    for s in  param['portfolio_dict']['Portfolio-'+str(n)].keys():
        param['portfolio_dict']['Portfolio-'+str(n)][s]['strategy'] = strategy_w_list[n].value
strategy_list = ['ma_breakout_strategy','mean_reversion_strategy']
for i in range(MAX_PORTFOLIO):
    strategy_w_list[i]=widgets.Dropdown(options=strategy_list,value=strategy_list[0],\
                                        decription='Strategy', layout={'width': '10%'}, style=style)
    strategy_w_list[i].observe(functools.partial(strategy_f, n=i), 'value')

def symbols_f(change, n=0):
    param['portfolio_dict']['Portfolio-'+str(n)] = {}
    #symbols_selected_w.options = param['portfolio_dict']['chori_strategy']
    symbols_select_w_list[n].value = ''
    for s in change.new:
        param['portfolio_dict']['Portfolio-'+str(n)][s] \
                = {'strategy' : strategy_w_list[n].value, 'trade_capital':trade_capital_w.value}
        param['indicator_dict']['Portfolio-'+str(n)][s] = default_indicator_list
    symbols_select_w_list[n].value = str(param['portfolio_dict']['Portfolio-'+str(n)])    


for i in range(MAX_PORTFOLIO):
    symbols_w_list[i] =widgets.SelectMultiple(
    options=symbol_short_list,
    value=[],
    #rows=10,
    description='Portfolio-'+str(i)+' Symbols',
    disabled=False, style=style
    )
    symbols_w_list[i].observe(functools.partial(symbols_f, n=i),'value')





def symbols_select_f(change, n=0):
    try:
        #print(change.new)
        param['portfolio_dict']['Portfolio-'+str(n)] = ast.literal_eval(change.new)
    except:
        #print('portfolio_dict:chori_strategy selection update error')
        pass
for i in range(MAX_PORTFOLIO):
    symbols_select_w_list[i] = widgets.Textarea(
        value='',
        #placeholder='',
        description='Portfolio-'+str(i)+' Selections',
        disabled=False
    )
    symbols_select_w_list[i].observe(functools.partial(symbols_select_f, n=i),'value')



def on_button_symbols_reset_clicked(b,n=0):
    symbols_w_list[n].value = []
    param['portfolio_dict']['Portfolio-'+str(n)] = {}
for i in range(MAX_PORTFOLIO):
    button_symbols_reset_w_list[i] = widgets.Button(description='Clear Portfolio-'+str(i)+' Selection',\
                                        display='flex', flex_flow='column',flex_wrap='wrap',\
                                        align_items='center',align_content='center',
                                       layout={'width': 'auto','height':'80px'})
    button_symbols_reset_w_list[i].on_click(functools.partial(on_button_symbols_reset_clicked,n=i))









'''
def symbols2_select_f(change):
    try:
        #print(change.new)
        param['portfolio_dict']['bros24_strategy'] = ast.literal_eval(change.new)
    except:
        #print('portfolio_dict:bros24_strategy selection update error')
        pass

symbols2_select_w = widgets.Textarea(
    value='',
    #placeholder='',
    description='Bros24 Selections',
    disabled=False
)
symbols2_select_w.observe(symbols2_select_f,'value')



def symbols2_f(change):
    param['portfolio_dict']['bros24_strategy'] = {}
    symbols2_select_w.value = ''
    for s in change.new:
        #symbols2_select_w.value += s+','
        param['portfolio_dict']['bros24_strategy'][s] = {"trade_capital":trade_capital_w.value}
        param['indicator_dict']['bros24_strategy'][s] = bros24_indicator_list
    symbols2_select_w.value = str(param['portfolio_dict']['bros24_strategy'])
    
symbols2_w =widgets.SelectMultiple(
    options=symbol_short_list,
    value=[],
    #rows=10,
    description='Bros24 Symbols',
    disabled=False, style=style
)
symbols2_w.observe(symbols2_f,'value')



button_symbols2_reset_w = widgets.Button(description="Clear Bros24 Symbol Selection", style=style, layout={'width': 'auto','height':'80px'})
def on_button_symbols2_reset_clicked(b):
    symbols2_w.value = []
    param['portfolio_dict']['bros24_strategy'] = {}
button_symbols2_reset_w.on_click(on_button_symbols2_reset_clicked)
'''

def use_SP500_w_f(change):
    if change.new is True:
        symbols_w.options = symbol_list
        symbols2_w.options = symbol_list
    else:
        symbols_w.options = symbol_short_list
        symbols2_w.options = symbol_short_list
use_SP500_w = widgets.Checkbox(
    value=False,
    description='Use SP500 Symbol List',
    disabled=False,
    indent=False
)
use_SP500_w.observe(use_SP500_w_f,'value')




param['show_detail_log'] = False
def show_detail_log_f(change):
    param['show_detail_log'] = change.new
show_detail_log_w = widgets.Checkbox(
    value=param['show_detail_log'],
    description='Show Log',
    disabled=False,
    indent=False
)
show_detail_log_w.observe(show_detail_log_f,'value')
#---------------------- system settings--------------------------------------------

'''
Direction of trade, in options, it's LONG->CALL option, SHORT->PUT option, 
BOTH->CALL and PUT option,  'LONG', 'SHORT', 'BOTH'
'''  

param['tradeDirection'] = 'BOTH'
def tradeDirection_f(tradeDirection):
    param['tradeDirection'] = tradeDirection_w.value
#tradeDirection_w = interactive(tradeDirection_f, tradeDirection=['BOTH','LONG','SHORT'])

tradeDirection_w=widgets.Dropdown(options=['BOTH','LONG','SHORT'],value='BOTH',\
                                  decription='Trade Direction', layout={'width': '10%'}, style=style)
tradeDirection_w.observe(tradeDirection_f, 'value')

#tradeDirection1=widgets.Dropdown(options=['BOTH','LONG','SHORT'], decription='Direction', layout={'width': '20%'})
#tradeDirection =widgets.SelectMultiple(
#    options=['Apples', 'Oranges', 'Pears'],
#    value=['Oranges'],
#    #rows=10,
#    description='Fruits',
#    disabled=False
#)


#def tradeDirection_f(tradeDirection):
#    param['tradeDirection'] = tradeDirection
#tradeDirection_w = interactive(tradeDirection_f, tradeDirection=['BOTH','LONG','SHORT'])
#tradeDirection_w.children[0].decription='Direction'
#tradeDirection_w.children[0].layout=Layout(width='80%')
#tradeDirection_w.manual = True
#tradeDirection_w.manual_name = "Direction"






param['RegularTargetProfit'] = 0.0
def RegularTargetProfit_f(change):
    param['RegularTargetProfit'] = change.new
RegularTargetProfit_w = widgets.FloatText(value=param['RegularTargetProfit'],description='TargetProfit(%)',disabled=False, layout={'width': bw}, style=style)
RegularTargetProfit_w.observe(RegularTargetProfit_f, 'value')


param['RegularStopLoss'] = 0.0
def RegularStopLoss_f(change):
    param['RegularStopLoss'] = change.new
RegularStopLoss_w = widgets.FloatText(value=param['RegularStopLoss'],description='StopLoss(%)',disabled=False, layout={'width': bw}, style=style)
RegularStopLoss_w.observe(RegularStopLoss_f, 'value')


param['TrailStopLoss'] = 0.0
def TrailStopLoss_f(change):
    param['TrailStopLoss'] = change.new
TrailStopLoss_w = widgets.FloatText(value=param['TrailStopLoss'],description='TrailStopLoss(%)',disabled=False, layout={'width': bw}, style=style)
TrailStopLoss_w.observe(TrailStopLoss_f, 'value')



''' Trading window for placing orders '''
param['useTradewindow'] = True
def useTradewindow_f(change):
    param['useTradewindow'] = change.new
useTradewindow_w = widgets.Checkbox(
    value=param['useTradewindow'],
    description='useTradewindow',
    disabled=False,
    indent=False
)
useTradewindow_w.observe(useTradewindow_f, 'value')


param['tradewindowStart'] = 930

def tradewindowStart1_f(change):
    param['tradewindowStart'] = 100*change.new+tradewindowStart2_w.value
tradewindowStart1_w = widgets.BoundedIntText(
    value=9,min=9,max=15,step=1,
    description='tradewindowStart',
    disabled=False,
    indent=False,layout={'width': '15%'}, style=style
)
tradewindowStart1_w.observe(tradewindowStart1_f, 'value')


def tradewindowStart2_f(change):
    param['tradewindowStart'] = 100*tradewindowStart1_w.value+change.new
tradewindowStart2_w = widgets.BoundedIntText(
    value=30,min=0,max=59,step=1,
    description='',
    disabled=False,
    indent=False,layout={'width': '40px'}, style=style
)
tradewindowStart2_w.observe(tradewindowStart2_f, 'value')






param['tradewindowEnd'] = 1555
'''
def tradewindowEnd_f(change):
    param['tradewindowEnd'] = change.new
tradewindowEnd_w = widgets.BoundedIntText(
    value=param['tradewindowEnd'],min=930,max=1559,step=1,
    description='tradewindowEnd',
    disabled=False,
    indent=False,layout={'width': '20%'}, style=style
)
tradewindowEnd_w.observe(tradewindowEnd_f, 'value')
'''
def tradewindowEnd1_f(change):
    param['tradewindowEnd'] = 100*change.new+tradewindowEnd2_w.value
tradewindowEnd1_w = widgets.BoundedIntText(
    value=15,min=9,max=15,step=1,
    description='tradewindowEnd',
    disabled=False,
    indent=False,layout={'width': '15%'}, style=style
)
tradewindowEnd1_w.observe(tradewindowEnd1_f, 'value')


def tradewindowEnd2_f(change):
    param['tradewindowEnd'] = 100*tradewindowEnd1_w.value+change.new
tradewindowEnd2_w = widgets.BoundedIntText(
    value=55,min=0,max=59,step=1,
    description='',
    disabled=False,
    indent=False,layout={'width': '40px'}, style=style
)
tradewindowEnd2_w.observe(tradewindowEnd2_f, 'value')




''' Intra-day squaring of positions'''
param['tradeSquare'] = True
def tradeSquare_f(change):
    param['tradeSquare'] = change.new
tradeSquare_w = widgets.Checkbox(
    value=param['tradeSquare'],
    description='Intraday tradeSquareOff',
    disabled=False,
    indent=False
)
tradeSquare_w.observe(tradeSquare_f, 'value')


param['tradeSquareTime'] = 1555
def tradeSquareTime1_f(change):
    param['tradeSquareTime'] = change.new*100+tradeSquareTime2_w.value
tradeSquareTime1_w = widgets.BoundedIntText(
    value=15,min=9,max=15,step=1,
    description='tradeSquareOffTime',
    disabled=False,
    indent=False,layout={'width': '18%'}, style=style
)
tradeSquareTime1_w.observe(tradeSquareTime1_f, 'value')


def tradeSquareTime2_f(change):
    param['tradeSquareTime'] = tradeSquareTime1_w.value*100+change.new
tradeSquareTime2_w = widgets.BoundedIntText(
    value=55,min=0,max=59,step=1,
    description='',
    disabled=False,
    indent=False,layout={'width': '40px'}, style=style
)
tradeSquareTime2_w.observe(tradeSquareTime2_f, 'value')


''' Strategy: ma_breakout_strategy, mean_reversion_strategy '''

''' 
Check for low volatility, 
default value in absence of symbol is True  
'''


param['useVolatility_dict'] = {"SPY":True,"TSLA":False,'AAPL':True,'AMZN':False}
param['volatility_switch_period'] = 14
param['ranging_period'] = 20

param['strategy'] = 'ma_breakout_strategy'

param['mean_reversion_period'] = 10
param['mean_reversion_secondary_period'] = 100
param['z_entry'] = 0.9
param['z_exit'] = 0.5


''' EMA crossing over/under SMA '''
param['useSMA'] = True
param['SMAPeriod'] = 10
def SMAPeriod_f(change):
    param['SMAPeriod'] = change.new
SMAPeriod_w = widgets.IntText(value=param['SMAPeriod'],description='SMAPeriod',disabled=False, layout={'width': bw}, style=style)
SMAPeriod_w.observe(SMAPeriod_f, 'value')


param['useEMA'] = True
param['EMAPeriod'] = 21
def EMAPeriod_f(change):
    param['EMAPeriod'] = change.new
EMAPeriod_w = widgets.IntText(value=param['EMAPeriod'],description='EMAPeriod',disabled=False, layout={'width': bw}, style=style)
EMAPeriod_w.observe(EMAPeriod_f, 'value')





#---------------------------------------------------------------------------------------------------------------------------------

'''spread constraint'''
param['maxOptionSpreadPercent'] = 1.0


'''
default lot size of each symbol, actual size will be 
calculated using trade_capital in portfolio_dict
'''
param['LOT_dict'] = {"SPY":1,"GOOG":1,"MED":1,"TSLA":1,'AAPL':1,'AMZN':1}

'''
RUN_FOR_MINUTES: Duration for loop (minutes), this value
should be set as 0 for backtesting on security
'''

param['RUN_FOR_MINUTES'] = 10
def RUN_FOR_MINUTES_f(change):
    param['RUN_FOR_MINUTES'] = change.new
RUN_FOR_MINUTES_w = widgets.IntText(value=param['RUN_FOR_MINUTES'],description='RUN_FOR_MINUTES',disabled=False, layout={'width': 'auto'}, style=style)
RUN_FOR_MINUTES_w.observe(RUN_FOR_MINUTES_f, 'value')




'BE CAREFUL! It will place live orders in your trade account (False/True)'
param['PLACE_ORDER'] = False
def PLACE_ORDER_f(change):
    param['PLACE_ORDER'] = change.new
PLACE_ORDER_w = widgets.Checkbox(
    value=param['PLACE_ORDER'],
    description='PLACE ORDER (BE CAREFUL! It will place live orders in your trade account)',
    disabled=False,
    indent=False,
    layout={'width': '100%'}
)
PLACE_ORDER_w.observe(PLACE_ORDER_f,'value')


'''
Following instrument list contains symbol to be traded
input is list like param['instrument_symbol_list'] =  ["SPY","TSLA","AAPL", "AMZN","GOOG","MED"]
'''

param['instrument_symbol_list'] = []

param['live_output'] = 'HTML:'
live_param['live_output'] = 'HTML:'

#-------------------------trader input settings --------------------------------


'update intra-bar tick data every N seconds'
param['UPDATE_TICK_DATA_SECONDS'] = 1


'paper trading in live market'
param['TRADE_LIVE'] = True


'allow short/put options'
param['ALLOW_SHORT'] = True


'generate refresh token every 90 days by switching it to True and then turn False again'
param['generate_refresh_token'] = False


#--------------------- time frame and history data paramters ---------------
param['timeframe']='minute'
def timeframe_f(timeframe):
    param['timeframe'] = timeframe
    if param['timeframe'] == 'daily':
        frequency_w.value = '1'
timeframe_w = interactive(timeframe_f, timeframe=['minute','daily'])

#1, 5, 10, 15, 30
param['frequency'] = '15'
def frequency_f(change):
    param['frequency'] = change.new
    if param['timeframe'] == 'daily':
        frequency_w.value = '1'
        #periodType_w.value = 'month'
#frequency_w = widgets.Text(value=param['frequency'],description='frequency',disabled=False, layout={'width': '15%'})
frequency_w = widgets.Dropdown(options=['1','5','10','15','30','60','240'],value='15', decription='frequency', layout={'width': '15%'}, style=style)
frequency_w.observe(frequency_f, 'value')




param['periodType']='day'
def periodType_f(periodType):
    param['periodType'] = periodType
periodType_w = interactive(periodType_f, periodType=['day','month'],layout={'width': '15%'})


param['period']='7'
def period_f(change):
    param['period'] = change.new
period_w = widgets.Text(value=param['period'],description='period',disabled=False, layout={'width': '15%'})
#period_w = widgets.Dropdown(options=['1','2','3','4','5','10'],value='10', decription='period', layout={'width': '15%'}, style=style)
period_w.observe(period_f, 'value')

param['extended_hours'] = True
def extended_hours_f(change):
    param['extended_hours'] = change.new
extended_hours_w = widgets.Checkbox(
    value=param['extended_hours'],
    description='extended hours',
    disabled=False,
    indent=False
)
extended_hours_w.observe(extended_hours_f, 'value')


param['multiframe'] = False
def multiframe_f(change):
    param['multiframe'] = change.new
multiframe_w = widgets.Checkbox(
    value=param['multiframe'],
    description='MULTIFRAME SYSTEM',
    disabled=False,
    indent=False
)
multiframe_w.observe(multiframe_f, 'value')


#---------------------------------post process------------------------------
param['liveOutputFrequency'] = 5

#print('param complete')
#--------------------------------------------------------------------------

param_original = param.copy()

button_param_reset_w = widgets.Button(description="Reset Parameters", style=style, layout={'width': 'auto','height':'80px'})
def on_button_param_reset_clicked(b):
    account_capital_w.value = param_original['account_capital']
    trade_capital_w.value = param_original['trade_capital']
    
    tradeDirection_w.value = 'BOTH'
    
    #symbols_w.value = []
    #param['portfolio_dict']['chori_strategy'] = {}
    
    
    useTradewindow_w.value = param_original['useTradewindow']
    tradewindowStart1_w.value = 9
    tradewindowStart2_w.value = 35
    tradewindowEnd1_w.value = 15
    tradewindowEnd1_w.value = 50
    
    tradeSquare_w.value = param_original['tradeSquare']
    tradeSquareTime1_w.value = 15
    tradeSquareTime2_w.value = 55
    
    timeframe_w.value = param_original['timeframe']
    frequency_w.value = param_original['frequency']
    period_w.value = param_original['period']
    periodType_w.value = param_original['periodType']
    
    
button_param_reset_w.on_click(on_button_param_reset_clicked)

'''
backtest_html_w = widgets.HTML(
    value="Hello <b>World</b>",
    placeholder='Some HTML',
    description='Some HTML',
)
'''



#fl = ['']
fl=['BACKTEST FILES']+glob.glob("./data/*BACKTEST.csv")
                
def backtest_files_f(change):
    #print(change.new)
    if change.new == '':
        return
    try:
        os.startfile(change.new)
    except:
        pass
test_layout = Layout(width='100%')
backtest_files_w = widgets.Select(
    options=fl,
    layout = test_layout,
    value='BACKTEST FILES',
    # rows=10,
    description='',
    disabled=False
)
#backtest_files_w.unobserve(backtest_files_f, 'value')
#backtest_files_w.options = fl
#backtest_files_w.value=''
backtest_files_w.observe(backtest_files_f,'value')






backtest_display_w = widgets.Textarea(
    value='',
    #placeholder='',
    description='Backtest Display',
    disabled=False
)
#backtest_display_w.observe(backtest_display_f,'value')

#reset_backtest = widgets.Output(layout={'border': '1px solid yellow', 'width':'100%'})


#def reset_backtest_f(change):
#    backtest_display_w.value = change.new
reset_backtest = widgets.Output(layout={'border': '1px solid yellow', 'width':'100%'})
#reset_backtest.observe(reset_backtest_f,'outputs')


button = widgets.Button(description="Run BackTest")
button.style.button_color = 'yellow'
output = widgets.Output()
#button_w = display(button, output)

@reset_backtest.capture(clear_output=True)
def on_button_clicked_thread(b):
    button.disabled = True
    if param['show_detail_log'] is True: print('running backtest with:',param)
    thread = Thread(target=on_button_clicked,args=(b,))
    thread.start()
    thread.join()
    button.disabled = False
def on_button_clicked(b):
    #print(param['ChoriSMAPeriod'])
    #return
    global portfolio_dict_chart
    global indicator_dict_chart
    global candles_dict_chart
    #with output:
    #portfolio_dict_chart = param['portfolio_dict']
    indicator_dict_chart = param['indicator_dict']
    backtest_param = param.copy()
    backtest_param['RUN_FOR_MINUTES'] = 0
    candles_dict_chart, portfolio_dict_chart, backtest_analysis_dict = run_system(backtest_param, None)
    
    fl = ['BACKTEST FILES']+glob.glob("./data/*BACKTEST.csv")
    backtest_files_w.options = fl
button.on_click(on_button_clicked_thread)





#-------------------OPTIMIZATION----------------------------------------------------
optimize_button = widgets.Button(description="Run Optimizer")
optimize_button.style.button_color = 'yellow'
#output = widgets.Output()
#button_w = display(button, output)

'''
@reset_backtest.capture(clear_output=True)
def on_optimize_button_clicked_thread(b):
    button.disabled = True
    if param['show_detail_log'] is True: print('running optimize with:',param)
    thread = Thread(target=on_optimize_button_clicked,args=(b,))
    thread.start()
    thread.join()
    button.disabled = False
'''    

param['SMA_LL'] = 10
param['SMA_HL'] = 50
param['SMA_STEP'] = 5 
param['EMA_LL'] = 3
param['EMA_HL'] = 21
param['EMA_STEP'] = 3

param['volatility_switch_period_LL'] = 14
param['volatility_switch_period_HL'] = 14
param['volatility_switch_period_STEP'] = 7

param['ranging_period_LL'] = 20
param['ranging_period_HL'] = 20
param['ranging_period_STEP'] = 5


reset_optimize = widgets.Output(layout={'border': '1px solid yellow', 'width':'100%'})
@reset_optimize.capture(clear_output=True)
def on_optimize_button_clicked(b):
    #print(param['ChoriSMAPeriod'])
    #return
    optimize_button.disabled = True
    
    Oparam = param.copy()
    
    Oparam['data_source'] = 'offline'
    
    #global portfolio_dict_chart
    #global indicator_dict_chart
    #global candles_dict_chart
    #with output:
    #portfolio_dict_chart = param['portfolio_dict']
    #indicator_dict_chart = param['indicator_dict']
    opcount=0
    dfo = pd.DataFrame() 
    dfo['SMAPeriod'] = np.nan
    dfo['EMAPeriod'] = np.nan
    dfo['volatility_switch_period'] = np.nan
    dfo['ranging_period'] = np.nan
    dfo['PnL'] = np.nan
    
    for i in range(Oparam['SMA_LL'],Oparam['SMA_HL']+Oparam['SMA_STEP'],Oparam['SMA_STEP']):
        for j in range(Oparam['EMA_LL'],Oparam['EMA_HL']+Oparam['EMA_STEP'],Oparam['EMA_STEP']):
            for k in range(Oparam['volatility_switch_period_LL'],\
                           Oparam['volatility_switch_period_HL']+Oparam['volatility_switch_period_STEP'],\
                           Oparam['volatility_switch_period_STEP']):
                for l in range(Oparam['ranging_period_LL'],\
                               Oparam['ranging_period_HL']+Oparam['ranging_period_STEP'],Oparam['ranging_period_STEP']):
                    
                    'loop start'
                    Oparam['SMAPeriod'] = i
                    Oparam['EMAPeriod'] = j
                    Oparam['volatility_switch_period'] = k
                    Oparam['ranging_period'] = l


                    backtest_param = Oparam.copy()
                    backtest_param['RUN_FOR_MINUTES'] = 0
                    candles_dict_, portfolio_dict_, backtest_analysis_dict = run_system(backtest_param, None)
                    print(backtest_analysis_dict)
                    @reset_backtest.capture(clear_output=False)
                    def show_optimization_result(c, Oparam, backtest_analysis_dict):
                        for portfolio in backtest_analysis_dict.keys():
                            symbols_dict = backtest_analysis_dict[portfolio]
                            for symbol in symbols_dict.keys():
                                try:
                                    PnL = symbols_dict[symbol]['PnL']
                                except:
                                    PnL = np.nan
                                dfo.at[c,'SMAPeriod'] = Oparam['SMAPeriod']
                                dfo.at[c,'EMAPeriod'] = Oparam['EMAPeriod']
                                dfo.at[c,'volatility_switch_period'] = Oparam['volatility_switch_period']
                                dfo.at[c,'ranging_period'] = Oparam['ranging_period']
                                dfo.at[c,'PnL'] = PnL
                                
                                try:
                                    dfo.to_csv('./data/'+portfolio+"_"+symbol+'_OPTIMIZATION.csv')
                                except:
                                    pass
                                
                                print(c,":OPTRUN: ","SMAPeriod",Oparam['SMAPeriod'],\
                                      " EMAPeriod",Oparam['EMAPeriod'],Oparam['volatility_switch_period'],Oparam['ranging_period'],\
                                      portfolio,":",symbol,":","PnL:",PnL)
                    show_optimization_result(opcount, Oparam, backtest_analysis_dict)
                    opcount+=1
                    'loop end'
    
    
    
    
    print('Optimization Complete')
    optimize_button.disabled = False
    #fl = ['BACKTEST FILES']+glob.glob("./data/*BACKTEST.csv")
    #backtest_files_w.options = fl
optimize_button.on_click(on_optimize_button_clicked)



'''
def backtest_f(x):
    global candles_dict
    if x:
        print('running backtest with:',param)
        candles_dict = run_system(param, None)
backtest_w = interact_manual(backtest_f,x=False)
backtest_w.manual = True
backtest_w.manual_name = "Run Backtest"
'''


global fig_dict
fig_dict = {}                   
chart = widgets.Button(description="BackTest Chart")
chart.style.button_color = 'lightblue'
chart_output = widgets.Output()
#display(chart, chart_output)
def on_charting(b):
    chart.disabled = True
    global fig_dict
    #with chart_output:
    #print(portfolio_dict_chart)
    #print(indicator_dict_chart)
    if True:
        if True:    
            for portfolio in portfolio_dict_chart:
                symbols = portfolio_dict_chart[portfolio]
                for symbol in symbols.keys():
                    indicator_list = indicator_dict_chart[portfolio][symbol]
                    fig_dict[portfolio+symbol] = plot_backtest_charts(portfolio=portfolio, symbol=symbol, \
                                 timeframe=param['timeframe'], frequency=param['frequency'], \
                                 periodType=param['periodType'], period=param['period'], \
                                 params=param, tradeDirection=param['tradeDirection'], 
                                 extended_hours=False, candles_dict=candles_dict_chart,indicator_list=indicator_list,\
                                                                     portfolio_dict=portfolio_dict_chart)
        else:
            print('charting failed')
    chart.disabled = False
    return
chart.on_click(on_charting)


reset_live = widgets.Output(layout={'border': '1px solid green', 'width':'100%'})

live_button = widgets.Button(description="Run Live!")
live_button.style.button_color = 'lightgreen'
#button_w = display(button, output)

#@reset_live.capture(clear_output=True)
def on_live_button_clicked_thread(b):
    live_button.disabled = True
    if param['show_detail_log'] is True: print('running live with:',param)
    live_thread = Thread(target=on_live_button_clicked,args=(b,))
    live_thread.start()
    #live_thread.join()
    #live_button.disabled = False


@reset_live.capture(clear_output=True)    
def on_live_button_clicked(b):
    #print(param['ChoriSMAPeriod'])
    #return
    global live_param
    global live_portfolio_dict_chart
    global live_indicator_dict_chart
    global live_candles_dict_chart
    #with output:
    #portfolio_dict_chart = param['portfolio_dict']
    live_indicator_dict_chart = param['indicator_dict']
    live_param = param.copy()
    #live_param['RUN_FOR_MINUTES'] = 500
    
    live_candles_dict_chart, live_portfolio_dict_chart = run_system(live_param, None)
    live_button.disabled = False
    #fl = ['']+glob.glob("./data/*BACKTEST.csv")
    #backtest_files_w.options = fl
live_button.on_click(on_live_button_clicked_thread)


stop_live_button = widgets.Button(description="Stop Live")
stop_live_button.style.button_color = 'red'


@reset_live.capture(clear_output=False)
def on_stop_live_button_clicked(b):
    print('STOPPING LIVE TRADE')
    global live_param
    live_param['RUN_FOR_MINUTES'] = 0
stop_live_button.on_click(on_stop_live_button_clicked)



generate_refresh_token_button = widgets.Button(description="Get Refresh Token")
generate_refresh_token_button.style.button_color = 'pink'
def on_generate_refresh_token_clicked(b):
    print('generating refresh token ')
    generate_refresh_token()
generate_refresh_token_button.on_click(on_generate_refresh_token_clicked)




#def account_f(change):
#    try:
        #print(change.new)
#        param['portfolio_dict']['bros24_strategy'] = ast.literal_eval(change.new)
#    except:
        #print('portfolio_dict:bros24_strategy selection update error')
#        pass
account_w = widgets.Textarea(
    value='',
    #placeholder='',
    description='Account Details',
    disabled=False,
    layout={'width':'100%'},)
#account_w.observe(account_f,'value')

print('fetching account details')
#try:
account_flag=0
accounts=get_account_detail()
if accounts is None:
    dl = [{'accountId':None,'accountType':None,\
           'isDayTrader':None,\
           'cashBalance':None,\
           'cashAvailableForTrading':None,\
           'cashAvailableForWithdrawal':None,\
          }]
else:    
    try:
        account=accounts[0]['securitiesAccount']
        dl = [{'accountId':account['accountId'],'accountType':account['type'],\
               'isDayTrader':account['isDayTrader'],\
               'cashBalance':account['currentBalances']['cashBalance'],\
               'cashAvailableForTrading':account['currentBalances']['cashAvailableForTrading'],\
               'cashAvailableForWithdrawal':account['currentBalances']['cashAvailableForWithdrawal'],\
              }]
        account_flag=1
        account_capital_w.value = account['currentBalances']['cashAvailableForTrading']
    except:
        account=accounts[0]['securitiesAccount']
        dl = [{'accountId':account['accountId'],'accountType':account['type'],\
               'isDayTrader':account['isDayTrader'],\
               'cashBalance':account['currentBalances']['cashBalance'],\
               'cashAvailableForTrading':account['currentBalances']['availableFunds'],\
             }]
        account_flag=1
        account_capital_w.value = account['currentBalances']['availableFunds']

if account_flag==0:
    dl = [{'accountId':None,'accountType':None,\
           'isDayTrader':None,\
           'cashBalance':None,\
           'cashAvailableForTrading':None,\
           'cashAvailableForWithdrawal':None,\
          }]

dfa  = pd.DataFrame(dl)


account_w.value = dfa.to_string()

account_capital_w.value = 10000.0

'''
position_list = []
try:
    position_list = get_positions()
except:
    pass
'''


    
#def html_f(change):
#    html_w.value = change.new
html_w = widgets.HTML(value=live_param['live_output'])
#html_w.observe(html_f,'value')

#--------------------create diplay box-------------------------------------
vbox_list = []

hbox11  = HBox([data_source_w,use_SP500_w,show_detail_log_w, button_param_reset_w, generate_refresh_token_button])
vbox_list.append(hbox11)

hbox12  = HBox([account_capital_w, tradeDirection_w, trade_capital_w])
vbox_list.append(hbox12)



portfolio_symbol_hbox_list=[None]*MAX_PORTFOLIO
for i in range(MAX_PORTFOLIO):
    portfolio_symbol_hbox_list[i] = HBox([strategy_w_list[i], symbols_w_list[i], symbols_select_w_list[i],button_symbols_reset_w_list[i]])
    vbox_list.append(portfolio_symbol_hbox_list[i])
    
#mabreakout_hbox = HBox([SMAPeriod_w, EMAPeriod_w])
#vbox_list.append(mabreakout_hbox)

hboxexitwindow = HBox([RegularTargetProfit_w, RegularStopLoss_w, TrailStopLoss_w])
vbox_list.append(hboxexitwindow)

hboxtradewindow = HBox([useTradewindow_w, tradewindowStart1_w, tradewindowStart2_w,tradewindowEnd1_w,tradewindowEnd2_w])
vbox_list.append(hboxtradewindow)

hboxtradesquare = HBox([tradeSquare_w, tradeSquareTime1_w, tradeSquareTime2_w])
vbox_list.append(hboxtradesquare)

data_history_hbox = HBox([timeframe_w,frequency_w,periodType_w,period_w,extended_hours_w]) 
vbox_list.append(data_history_hbox)

data_history_hbox = HBox([multiframe_w]) 
vbox_list.append(data_history_hbox)

#hbox7 = HBox([button, chart, backtest_files_w])
#hbox8 = HBox([live_button, stop_live_button, RUN_FOR_MINUTES_w, PLACE_ORDER_w])

#backtest_out_hbox = HBox([reset_backtest])
#live_out_hbox = HBox([reset_live])
#hbox102 = HBox([html_w])

backtest_box = VBox([HBox([button, chart, optimize_button]),HBox([backtest_files_w]), HBox([reset_backtest])])
live_box = VBox([HBox([live_button, stop_live_button]), HBox([RUN_FOR_MINUTES_w]), HBox([PLACE_ORDER_w]), HBox([reset_live])])
account_box = HBox([account_w])


#from ipywidgets import widgets
tab_contents = ['Backtest', 'Live', 'Account']
#children = [widgets.Text(description=name) for name in tab_contents]
tab = widgets.Tab()
tab.children = [backtest_box, live_box, account_box]
#tab.titles = [str(i) for i in range(len(tab_contents))]
tab.set_title(0, 'BackTest')
tab.set_title(1, 'Live')
tab.set_title(2, 'Account')

vbox_list.append(tab)
#system_box = HBox([backtest_box, live_box])

Box = VBox(vbox_list)


#END
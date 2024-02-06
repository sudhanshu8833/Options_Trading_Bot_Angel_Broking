import ccxt
import pandas as pd
from pprint import pprint
from finta import TA
from datetime import datetime
bybit=ccxt.bybit({
    'apiKey':"39fXkItRX2jEGVPcqw",
    "secret":"SlvDKa2Tjo4YYSe6G7mRrS0DMxTt3JL7rFVJ",
    'testnet':False
})

# print(bybit.fetch_balance())
balances=bybit.fetch_free_balance()
print(balances)
# price=bybit.fetch_ticker("BTC/USDT")['ask']
# print(price)
# # data=bybit.create_order("BTC/USDT","market","sell",.0002,price)
# data=bybit.create_market_sell_order("BTC/USDT",balances['BTC'])
# print(data)

# bybit.create_
# bybit.verbose = True
# data=bybit.create_order("BTC/USDT", "market", "sell", 0.00023174623846, 40000)
# data=bybit.create_market_sell_order("BTC/USDT",balances['BTC'])
# bybit.create_market_buy_order("BTC/USDT",10)
# print(data)
# pprint(bybit.create_order("BTC/USDT","market","sell",amount=balances['BTC'],price=40000))


# loops=1000
# while(loops):
#     data=bybit.fetch_ohlcv("ETH/USDT",timeframe='1m')

#     df=pd.DataFrame(data,columns=['Datetime','open','high','low','close','volume'])

#     print(datetime.fromtimestamp(df['Datetime'].iloc[-1]/1000),df['close'].iloc[-1])
#     loops-=1
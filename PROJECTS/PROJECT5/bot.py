# generic modules
from datetime import date
from typing import Final
import pandas as pd
import time
import sys

# local modules
from binance.client import Client
from binance.enums import *
from indicator import indicators

# local file
import secrets
from config import conf

# size of each candle for calculating SMA's open and close price 
KLINE_INTERVAL = "15m"
TIME_TO_SLEEP_API_RATE = 1
NUM_CANDLES = 20
ATR = conf["atr"]
FACTOR = conf["factor"]

class BinanceBot:

    def __init__(self):
        self.client = Client(secrets.binance_api_key, secrets.binance_api_secret_key)
        print("Logged in Binance Successfully!")
        self.data = {
                    "data": {
                         "candles": [
                            [

                            ]
                        ]
                    }
                    }
        self.parse()
        self.set_candles()
        # adds at first so we can remove after
        self.add_candles(num_candles=NUM_CANDLES)
        self.trade()


    def parse(self):
        main_symbol = conf["token"].upper()
        base_symbol = conf["base_token"].upper()
        self.symbol = main_symbol + base_symbol
        self.quantity = conf["quantity"]
        self.take_profit_percentage = conf["take_profit_precentage"]
        self.stop_loss_percentage = conf["stop_loss_precentage"]
       
    
    def trade(self):
        while True:
            try:
                self.handle_buy()
                self.handle_sell()
            except KeyboardInterrupt:
                print('Terminated the bot.')
                sys.exit(1)


    def handle_buy(self):
        print("Searching for a selling opportunity... To terminate the bot press CTRL^C")
        bought = False

        while not bought:
            last_candle_price = self.get_last_candle_close_price()
            time.sleep(TIME_TO_SLEEP_API_RATE)
            if self.buy_logic():
                if self.buy_spot():
                    print("{} bought {} {} at {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), self.quantity, self.symbol, last_candle_price))
                    bought = True


    """ 1 senerio we buy:
    1. supertrend becomes green
    """        
    def buy_logic(self):
        if self.get_signal() == "buy":
            return True
        return False


    def handle_sell(self):
        print("Searching for a selling opportunity... To terminate the bot press CTRL^C")
        sold = False

        while not sold:
            last_candle_price = self.get_last_candle_close_price()
            time.sleep(TIME_TO_SLEEP_API_RATE)
            
            if self.sell_logic():
                if self.sell_spot():
                    print("{} sold {} {} at {}".format(time.strftime("%Y-%m-%d %H:%M:%S"), self.quantity, self.symbol, last_candle_price))
                    sold = True
                continue
        

    """ 3 senerios we sell:
    1. take profit
    2. stop loss
    3. supertrend becomes red
    """        
    def sell_logic(self):
        last_candle_price = self.get_last_candle_close_price()
        candle_change_since_bought = self.get_candle_precent(last_candle_price, self.bought_price)

        if candle_change_since_bought > self.take_profit_percentage or \
            abs(1 - candle_change_since_bought) > self.stop_loss_percentage or \
            self.get_signal() == "sell":
            return True
        return False


    """ buy crypto in spot account
    """
    def buy_spot(self):
        try:
            buy_order  = self.client.create_order(
                symbol = self.symbol,
                side = SIDE_BUY,
                type = ORDER_TYPE_MARKET,
                quantity = self.quantity,
            )
            return True

        except Exception as e:
            print(e)
            return False


    """ sell crypto in spot account
    """
    def sell_spot(self):
        try:
            sell_order  = self.client.create_order(
                symbol = self.symbol,
                side = SIDE_SELL,
                type = ORDER_TYPE_MARKET,
                quantity = self.quantity,
            )
            return True

        except Exception as e:
            print(e)
            return False


    """ gets last candle close price
    """
    def get_last_candle_close_price(self):
        return self.df.iloc[-1]["Close"]


    """ returns a candle percentge change
    """
    def get_candle_precent(self, close_price, open_price):
        return (close_price / open_price - 1) * 100


    """ returns a list of lists that contains # Open
    # Open time
    # Open 
    # High
    # Low
    # Close
    # Volume

    Gets new candle every 15 minutes according to KLINE_INTERVAL constant
    but get new close price of last candle
    """
    def get_candles(self, symbol= None, num_limit = 1):
        klines = self.client.get_klines(symbol=symbol, interval=KLINE_INTERVAL, limit=num_limit)
        final_klines = []
        for kline in klines:
            sorted_kline = kline[:6]
            temp_kline = []
            for k in sorted_kline:
                temp_kline.append(float(k))
            final_klines.append(temp_kline)
        return final_klines


    """ sets the first candle of the df
        called once in __init__
    """
    def set_candles(self):
        self.data["data"]["candles"][0] = self.get_candles(self.symbol, num_limit=1)[0]
        
        self.fetch_candles_to_df()


    """ gets candles and adds them to data
    and then fetches them with fetch_candles_to_df function
    called every loop in buy or sell logic
    """
    def add_candles(self, num_candles):
        candles = self.get_candles(self.symbol, num_limit=num_candles)
        for i in range(len(candles)):
            self.data["data"]["candles"].append(candles[i])
        self.fetch_candles_to_df()


    """ removes oldest candles from df
    and oldest candles from data
    """
    def remove_candles(self, num_candles):
        self.data["data"]["candles"] = self.data["data"]["candles"][NUM_CANDLES:]
        self.df = self.df.iloc[num_candles:]


    """ updates df with our new candles from data
    """
    def fetch_candles_to_df(self):
        self.df = pd.DataFrame(self.data["data"]["candles"], columns=['date', 'Open', 'High', 'Low', 'Close', 'volume'])
        print(self.df)

    """ add candle to df and remove old ones
    """
    def handle_candles(self):
        self.add_candles(num_candles=NUM_CANDLES)
        self.remove_candles(num_candles=NUM_CANDLES)


    """ returns buy or sell signal
    """
    def get_signal(self):
        new_df = indicators.SuperTrend(self.df, ATR, FACTOR)
        # adds and removes candles
        self.handle_candles()
        # singal is up (buy) or down (sell)
        signal = new_df.iloc[-1]['STX_{}_{}'.format(ATR, FACTOR)]
        return signal


def main():
    BinanceBot()


main()

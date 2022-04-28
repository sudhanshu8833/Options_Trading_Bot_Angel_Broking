# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import time
import numpy as np
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import pandas as pd
df3 = pd.read_csv("parameters.csv")
df3.set_index("parameters",inplace=True)
df1=df3.T

import telepot
bot = telepot.Bot('2036653591:AAGFldTooJ3wc7Cao1gRc6YxbqKABc4ncBI')
bot.getMe()

# %%

accesstoken=df1['access_token']['value0']
client = oandapyV20.API(access_token=str(accesstoken))
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
account_id = str(df1['account_id']['value0'])
# import telepot
# bot = telepot.Bot('2039634255:AAHuSFIcnPpS-4u6dxJKoJQ34R271J1v59s')
# bot.getMe()

# %%

# client = oandapyV20.API(access_token="5feaa802c52be3e714d4bd74bc1a9169-8cbadb5f1a922e05aad7d56841b3f44a")
# account_id="101-002-19512089-001"


# %%
df3 = pd.read_csv("parameters.csv")
df3.set_index("parameters",inplace=True)
df1=df3.T


# %%
def candle(instrument):
    global df1,account_id

    params = {"count": 150,"granularity":str(df1['time_frame']['value0'])} #granularity can be in seconds S5 - S30, minutes M1 - M30, hours H1 - H12, days D, weeks W or months M
    candles = instruments.InstrumentsCandles(instrument=instrument,params=params)
    client.request(candles)
    #print(candles.response)
    ohlc_dict = candles.response["candles"]
    ohlc = pd.DataFrame(ohlc_dict)
    ohlc_df = ohlc.mid.dropna().apply(pd.Series)
    ohlc_df["volume"] = ohlc["volume"]
    ohlc_df.index = ohlc["time"]
    ohlc_df = ohlc_df.apply(pd.to_numeric)
    ohlc_df = ohlc_df.rename(columns = {'o': 'Open', 'h': 'High','l':'Low','c':'Close','volume':'Volume'})

    return ohlc_df[:-1]


# %%
def ltp_price(instrument):
    params = {"instruments": str(instrument)}
    r = pricing.PricingInfo(accountID=account_id, params=params)
    rv = client.request(r)
    EUR_USD=float(rv["prices"][0]["closeoutBid"])

    return EUR_USD


# %%
def market_order(instrument):
        global df1,account_id
        r = accounts.AccountSummary(accountID=account_id)
        client.request(r)

        data=r.response
        balance=float(data['account']['balance'])*float(df1['leverage']['value0'])
        ltp=ltp_price(instrument)
        quantity=int(balance/ltp)


        try:
            data = {
                    "order": {

                    "timeInForce": "FOK",
                    "instrument":str(instrument),
                    "units": str(quantity),
                    "type": "MARKET",
                    "positionFill": "DEFAULT"
                            }
                    }
            
            r = orders.OrderCreate(accountID=account_id, data=data)
            client.request(r)
        except Exception as e:
            print(str(e))
            bot.sendMessage(1190128536,str(e))

        bot.sendMessage(1190128536,f'buyed stock at{ltp} quantity of {quantity}')
        


def market_order1(instrument):
        global df1,account_id
        r = accounts.AccountSummary(accountID=account_id)
        client.request(r)
        # print(r.response)
        data=r.response
        balance=float(data['account']['balance'])*float(df1['leverage']['value0'])
        ltp=ltp_price(instrument)
        quantity=int(balance/ltp)





        try:
            data = {
                    "order": {

                    "timeInForce": "FOK",
                    "instrument": str(instrument),
                    "units": str(quantity*-1),
                    "type": "MARKET",
                    "positionFill": "DEFAULT"
                            }
                    }
            
            r = orders.OrderCreate(accountID=account_id, data=data)
            client.request(r)
        except Exception as e:
            print(str(e))
            bot.sendMessage(1190128536,str(e))
            

        bot.sendMessage(1190128536,f'sold stock at {ltp} quantity of {quantity}')
        


# %%
def main():
    global df1,l,X,account_id,position

    df3 = pd.read_csv("parameters.csv")
    df3.set_index("parameters",inplace=True)
    df1=df3.T

    df=candle(str(df1['symbol']['value0']))
    print(df)

    if l==0:
        print('hi')
        X=float(df1['X']['value0'])
        ltp=ltp_price(df1['symbol']['value0'])
        if ltp>X:
            while True:
                try:
                    times1=time.time()
                    print('hi')
                    df=candle(str(df1['symbol']['value0']))
                    bot.sendMessage(1190128536,f'{X} and ltp is {df["Close"][-1]} with position {position}')
                    if float(df['Close'].iloc[-1])<X:
                        market_order1(df1['symbol']['value0'])
                        l=1
                        position='short'
                        break
                    else:
                        time.sleep(60*float(df1['time']['value0'])-(time.time()-times1))
                except Exception as e:
                    print(str(e))
                    bot.sendMessage(1190128536,str(e))
                    

        elif ltp<X:
            while True:
                try:
                    times1=time.time()
                    df=candle(str(df1['symbol']['value0']))
                    bot.sendMessage(1190128536,f'{X} and ltp is {df["Close"][-1]} with position {position}')
                    if float(df['Close'].iloc[-1])>X:
                        market_order(df1['symbol']['value0'])
                        position='long'
                        l=1
                        break
                    else:
                        time.sleep(60*float(df1['time']['value0'])-(time.time()-times1))
                except Exception as e:
                    print(str(e))
                    bot.sendMessage(1190128536,str(e))

    if l==1:
        while True:
            try:
                times1=time.time()
                df=candle(str(df1['symbol']['value0']))
                # ltp=ltp_price(df1['symbol']['value0'])
                bot.sendMessage(1190128536,f'{X} and ltp is {df["Close"][-1]} with position {position}')
                if float(df['High'].iloc[-1])>X+float(df1['Y_offset']['value0']) and position=='long':
                    X=X+float(df1['Y_offset']['value0'])
                    market_order1(df1['symbol']['value0'])
                    position=''
                    time.sleep(60*float(df1['time']['value0'])-(time.time()-times1))

                elif float(df['Close'].iloc[-1])<X and position=='long':
                    market_order1(df1['symbol']['value0'])
                    market_order1(df1['symbol']['value0'])
                    position='short'
                    time.sleep(60*float(df1['time']['value0'])-(time.time()-times1))


                elif float(df['High'].iloc[-1])<X-float(df1['Y_offset']['value0']) and position=='short':
                    X=X-float(df1['Y_offset']['value0'])
                    market_order(df1['symbol']['value0'])
                    position=''
                    time.sleep(60*float(df1['time']['value0'])-(time.time()-times1))

                elif float(df['Close'].iloc[-1])>X and position=='short':
                    market_order(df1['symbol']['value0'])
                    market_order(df1['symbol']['value0'])
                    position='long'
                    time.sleep(60*float(df1['time']['value0'])-(time.time()-times1))
                else:
                    time.sleep(60*float(df1['time']['value0'])-(time.time()-times1))
            except Exception as e:
                print(str(e))
                bot.sendMessage(1190128536,str(e))
        






# %%
l=0
position=''

while True:
    times1=time.time()
    try:
    
        main()

    except Exception as e:
        bot.sendMessage(1190128536,str(e))

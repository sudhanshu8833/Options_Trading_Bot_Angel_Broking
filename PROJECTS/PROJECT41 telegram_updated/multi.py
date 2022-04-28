# %%
# importing the threading module


from datetime import date
import pandas as pd
import time
import sys
# local modules

from binance.client import Client
from binance.enums import *
from indicator import indicators

# local file
import traceback
import secrets
import json
import yfinance as yf
import numpy as np
import datetime as dt
import requests
import json
import pandas as pd
import numpy as np
import requests
import time
import urllib
from finta import TA
from multiprocessing import Process
from binance.client import BaseClient
import threading
import telepot
import pandas as pd
bot = telepot.Bot('5315492645:AAGh3s_DzaH2vazMkltWcH-9d3JBuLnXGNA')
bot.getMe()

BaseClient.FUTURES_TESTNET_URL = 'https://fapi.binance.{}/fapi'
BaseClient.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'

client = Client("cc9feab03d1264ed67c07738cdd42502dd80a8b67fedaf2e5f9b6e9c55a2faad",
                "e30d3db72358639f29b6280bf1c54fd564e7b1eb5cb13f020739fd197f396e1b")

# import pandas as pd
# bot = telepot.Bot('1715056219:AAGxytb3U1gIt1vlVn8Jf5b4za3E1HPuOd4')
# bot.getMe()
bot.sendMessage(1039725953, "hi")


def ltp_price(instrument):
    prices = client.get_all_tickers()
    for i in range(len(prices)):
        if prices[i]['symbol'] == str(instrument):

            return float(prices[i]['price'])


# %%
df3 = pd.read_csv("account1.csv")
# df3.set_index("parameters",inplace=True)
# df2=df3.T
dictionary = {}


account1 = []
for i in range(len(df3)):
    api_key = df3['api key'][i]
    api_secret_key = df3['api secret key'][i]
    client = Client(str(api_key), str(api_secret_key))
    account1.append(client)
    dictionary[str(client)] = api_key

df3 = pd.read_csv("account2.csv")

account2 = []
for i in range(len(df3)):
    api_key = df3['api key'][i]
    api_secret_key = df3['api secret key'][i]
    client = Client(str(api_key), str(api_secret_key))
    account2.append(client)
    dictionary[str(client)] = api_key
df3 = pd.read_csv("account3.csv")

account3 = []
for i in range(len(df3)):
    api_key = df3['api key'][i]
    api_secret_key = df3['api secret key'][i]
    client = Client(str(api_key), str(api_secret_key))
    account3.append(client)
    dictionary[str(client)] = api_key

df3 = pd.read_csv("account4.csv")

account4 = []
for i in range(len(df3)):
    api_key = df3['api key'][i]
    api_secret_key = df3['api secret key'][i]
    client = Client(str(api_key), str(api_secret_key))
    account4.append(client)
    dictionary[str(client)] = api_key


def get_precision(symbol):
    global info
    for x in info['symbols']:
        if x['symbol'] == symbol:
            return x['quantityPrecision']


j = 0


def main(name, values, orders, value, dictionary):
    global j
    while True:
        try:
            for order in orders:
                ltp = ltp_price(order['symbol'])
                # print(order)
                try:
                    if order['side'] == 'short':
                        if ltp >= float(order['stoploss']) or ltp <= float(order['takeprofit']):

                            for client in name:

                                for key, value in order['quantity']:
                                    if str(client) == str(key):
                                        quantity = value
                                        break

                                order1 = client.futures_create_order(
                                    symbol=str(order['symbol']),
                                    side=Client.SIDE_BUY,
                                    type=Client.ORDER_TYPE_MARKET,

                                    quantity=quantity)

                            orders.remove(order)
                            bot.sendMessage(
                                1039725953, f"squarred off the short position of {order['symbol']}")

                    if order['side'] == 'long':
                        if ltp <= float(order['stoploss']) or ltp >= float(order['takeprofit']):

                            for client in name:

                                for key, value in order['quantity']:
                                    if str(client) == str(key):
                                        quantity = value
                                        break

                                order1 = client.futures_create_order(
                                    symbol=str(order['symbol']),
                                    side=Client.SIDE_SELL,
                                    type=Client.ORDER_TYPE_MARKET,

                                    quantity=quantity)
                            orders.remove(order)
                            bot.sendMessage(
                                1039725953, f"squarred off the long position of {order['symbol']}")

                except Exception as e:
                    bot.sendMessage(1039725953, str(traceback.format_exc()))

            from pprint import pprint
            while True:
                try:
                    response = bot.getUpdates()
                except:
                    continue

                break
            if len(response) > j:
                if 'document' in response[-1]['message']:
                    print(response)
                    # if response[-1]['message']['document']['file_name'].upper()=='STOCKS.CSV':

                    #     file_id=response[-1]['message']['document']['file_id']

                    #     endpoint=r"https://api.telegram.org/bot1715056219:AAGxytb3U1gIt1vlVn8Jf5b4za3E1HPuOd4/getFile?file_id={}".format(file_id)
                    #     content=requests.get(url=endpoint)
                    #     content=content.json()

                    #     file_path=content['result']['file_path']
                    #     endpoint=r"https://api.telegram.org/file/bot1715056219:AAGxytb3U1gIt1vlVn8Jf5b4za3E1HPuOd4/{}".format(file_path)
                    #     req = requests.get(endpoint)
                    #     url_content = req.content
                    #     csv_file = open('stocks.csv', 'wb')

                    #     csv_file.write(url_content)
                    #     csv_file.close()

                    #     bot.sendDocument(1039725953, document=open('stocks.csv', 'rb'))
                    #     bot.sendMessage(1039725953,'please veriy if the stocks are updated or not')

                    if response[-1]['message']['document']['file_name'].upper() == 'PARAMETERS.CSV':
                        file_id = response[-1]['message']['document']['file_id']

                        endpoint = r"https://api.telegram.org/bot5315492645:AAGh3s_DzaH2vazMkltWcH-9d3JBuLnXGNA/getFile?file_id={}".format(
                            file_id)
                        content = requests.get(url=endpoint)
                        content = content.json()
                        file_path = content['result']['file_path']
                        endpoint = r"https://api.telegram.org/file/bot5315492645:AAGh3s_DzaH2vazMkltWcH-9d3JBuLnXGNA/{}".format(
                            file_path)
                        req = requests.get(endpoint)
                        url_content = req.content
                        csv_file = open('parameters.csv', 'wb')

                        csv_file.write(url_content)
                        csv_file.close()

                        bot.sendDocument(1039725953, document=open(
                            'parameters.csv', 'rb'))
                        # bot.sendDocument(1851811921, document=open('parameters.csv', 'rb'))
                        bot.sendMessage(
                            1039725953, 'please veriy if the parameters are updated or not')
                        # bot.sendMessage(1851811921,'please veriy if the parameters are updated or not')

                else:

                    message = response[-1]['message']['text']

                    message = message.upper()
                    print(message)

                    if message == 'SEE PARAMETERS' and value == 'account1':

                        bot.sendDocument(1039725953, document=open(
                            'parameters.csv', 'rb'))

                    if message == 'SEE ACCOUNTS':

                        bot.sendDocument(1039725953, document=open(
                            str(value)+'.csv', 'rb'))

                    if message == 'SEE PORTFOLIO':
                        address = []
                        money = []

                        for client in name:
                            data = client.futures_account_balance()
                            for i in range(len(data)):
                                if data[i]['asset'] == 'USDT':
                                    p_l = float(data[i]['withdrawAvailable'])
                                    address.append(dictionary[str(client)])
                                    money.append(p_l)

                        df = pd.DataFrame(list(zip(address, money)),
                                          columns=['client_id', 'portfolio'])
                        df.to_csv('portfolio_'+str(value)+'.csv')

                        bot.sendDocument(1039725953, document=open(
                            'portfolio_'+str(value)+'.csv', 'rb'))

                    message = message.split(' ')

                    if 'FLB' in message[0] and len(message) == 3:
                        stock = str(message[1])
                        price = str(message[2])

                        for client in name:
                            data = client.futures_account_balance()
                            for i in range(len(data)):
                                if data[i]['asset'] == 'USDT':
                                    p_l = float(data[i]['withdrawAvailable'])

                            quantity = (
                                ((float(values[0]))/100) * p_l)/float(price)

                            quantity = float(quantity*values[3])
                            precision = int(get_precision(str(stock)))
                            client.futures_change_leverage(
                                symbol=str(stock), leverage=int(values[3]))

                            print(quantity)

                            try:
                                order1 = client.futures_create_order(
                                    symbol=str(stock),
                                    side=Client.SIDE_BUY,
                                    type=Client.ORDER_TYPE_LIMIT,
                                    price=str(price),
                                    timeInForce='GTC',
                                    quantity=round(quantity, precision))

                            except Exception as e:
                                bot.sendMessage(1039725953, str(
                                    traceback.format_exc()))

                        bot.sendMessage(1039725953, 'order confirmed')

                    if 'FLS' in message[0] and len(message) == 3:
                        stock = str(message[1])
                        price = str(message[2])

                        for client in name:
                            data = client.futures_account_balance()
                            for i in range(len(data)):
                                if data[i]['asset'] == 'USDT':
                                    p_l = float(data[i]['withdrawAvailable'])

                            quantity = (
                                ((float(values[0]))/100) * p_l)/float(price)

                            quantity = float(quantity*values[3])
                            precision = int(get_precision(str(stock)))
                            client.futures_change_leverage(
                                symbol=str(stock), leverage=int(values[3]))

                            print(quantity)

                            try:
                                order1 = client.futures_create_order(
                                    symbol=str(stock),
                                    side=Client.SIDE_SELL,
                                    type=Client.ORDER_TYPE_LIMIT,
                                    price=str(price),
                                    timeInForce='GTC',
                                    quantity=round(quantity, precision))
                            except Exception as e:
                                bot.sendMessage(1039725953, str(
                                    traceback.format_exc()))

                        bot.sendMessage(1039725953, 'order confirmed')

                    if 'FMB' in message[0] and len(message) == 3:
                        stock = str(message[1])
                        ltp = ltp_price(str(stock))

                        order = {}
                        order['quantity'] = {}

                        for client in name:
                            data = client.futures_account_balance()
                            for i in range(len(data)):
                                if data[i]['asset'] == 'USDT':
                                    p_l = float(data[i]['withdrawAvailable'])

                            quantity = (
                                ((float(values[0]))/100) * p_l)/float(ltp)

                            quantity = float(quantity*values[3])
                            precision = int(get_precision(str(stock)))
                            client.futures_change_leverage(
                                symbol=str(stock), leverage=int(values[3]))
                            order['quantity'][str(client)] = round(
                                quantity, precision)

                            print(quantity)

                            try:
                                order1 = client.futures_create_order(
                                    symbol=str(stock),
                                    side=Client.SIDE_BUY,
                                    type=Client.ORDER_TYPE_MARKET,

                                    quantity=round(quantity, precision))

                            except Exception as e:
                                bot.sendMessage(1039725953, str(
                                    traceback.format_exc()))

                        order['symbol'] = stock
                        order['price'] = ltp
                        order['side'] = 'long'

                        order['type'] = 'market'
                        order['stoploss'] = float(ltp)*(1-(values[1])/100)
                        order['takeprofit'] = float(ltp)*(1+(values[2])/100)
                        bot.sendMessage(1039725953, str(order))
                        orders.append(order)

                    if 'FMS' in message[0] and len(message) == 3:
                        stock = str(message[1])
                        ltp = ltp_price(str(stock))

                        order = {}
                        order['quantity'] = {}
                        for client in name:
                            data = client.futures_account_balance()
                            for i in range(len(data)):
                                if data[i]['asset'] == 'USDT':
                                    p_l = float(data[i]['withdrawAvailable'])

                            quantity = (
                                ((float(values[0]))/100) * p_l)/float(ltp)

                            quantity = float(quantity*values[3])
                            precision = int(get_precision(str(stock)))
                            order['quantity'][str(client)] = round(
                                quantity, precision)
                            client.futures_change_leverage(
                                symbol=str(stock), leverage=int(values[3]))

                            print(quantity)

                            try:

                                order1 = client.futures_create_order(
                                    symbol=str(stock),
                                    side=Client.SIDE_SELL,
                                    type=Client.ORDER_TYPE_MARKET,
                                    quantity=round(quantity, precision))

                            except Exception as e:
                                # print(str(traceback.format_exc()))
                                bot.sendMessage(1039725953, str(
                                    traceback.format_exc()))

                        order['symbol'] = stock
                        order['price'] = ltp
                        order['side'] = 'short'
                        order['type'] = 'market'
                        order['stoploss'] = float(
                            ltp)*(1+(float(values[1]))/100)
                        order['takeprofit'] = float(
                            ltp)*(1-(float(values[2]))/100)
                        bot.sendMessage(1039725953, str(order))
                        orders.append(order)

                    if 'FMB2' in message[0]:
                        stock = str(message[1])
                        ltp = ltp_price(str(stock))

                        for client in name:
                            data = client.futures_account_balance()
                            for i in range(len(data)):
                                if data[i]['asset'] == 'USDT':
                                    p_l = float(data[i]['withdrawAvailable'])

                            quantity = (
                                ((float(values[0]))/100) * p_l)/float(ltp)

                            quantity = float(quantity*values[3])
                            precision = int(get_precision(str(stock)))
                            client.futures_change_leverage(
                                symbol=str(stock), leverage=int(values[3]))

                            print(quantity)

                            try:
                                order1 = client.futures_create_order(
                                    symbol=str(stock),
                                    side=Client.SIDE_BUY,
                                    type=Client.ORDER_TYPE_MARKET,

                                    quantity=round(quantity, precision))

                            except Exception as e:
                                bot.sendMessage(1039725953, str(
                                    traceback.format_exc()))
                        if value == 'account1':
                            bot.sendMessage(
                                1039725953, f'order placed for {stock} at {ltp}')

                    if 'FMS2' in message[0]:
                        stock = str(message[1])
                        ltp = ltp_price(str(stock))

                        for client in name:
                            data = client.futures_account_balance()
                            for i in range(len(data)):
                                if data[i]['asset'] == 'USDT':
                                    p_l = float(data[i]['withdrawAvailable'])

                            quantity = (
                                ((float(values[0]))/100) * p_l)/float(ltp)

                            quantity = float(quantity*values[3])
                            precision = int(get_precision(str(stock)))

                            client.futures_change_leverage(
                                symbol=str(stock), leverage=int(values[3]))

                            print(quantity)

                            try:

                                order1 = client.futures_create_order(
                                    symbol=str(stock),
                                    side=Client.SIDE_SELL,
                                    type=Client.ORDER_TYPE_MARKET,
                                    quantity=round(quantity, precision))

                            except Exception as e:
                                # print(str(traceback.format_exc()))
                                bot.sendMessage(1039725953, str(
                                    traceback.format_exc()))

                        if value == 'account1':
                            bot.sendMessage(
                                1039725953, f'order placed for {stock} at {ltp}')
    ##########SPOT#######################################################################
    ##########SPOT#######################################################################
    ##########SPOT#######################################################################
    ##########SPOT#######################################################################
                    # if 'SLB' in message[0]:
                    #     stock=str(message[1])
                    #     price=str(message[2])

                    #     for client in name:
                    #         data=client.get_account_snapshot(type='SPOT')
                    #         wallet=data['snapshotVos'][0]['data']['balances']
                    #         for i in wallet:
                    #             if i['asset']=='USDT':
                    #                 print(i)
                    #                 p_l=i['free']
                    #                 break

                    #         quantity=(((float(values[0]))/100) * p_l)/float(price)

                    #         quantity=float(quantity)
                    #         precision=int(get_precision(str(stock)))

                    #         order = client.create_order(
                    #             symbol=str(stock),
                    #             side=Client.SIDE_BUY,
                    #             type=Client.ORDER_TYPE_LIMIT,
                    #             price=str(price),
                    #             timeInForce='GTC',
                    #             quantity=round(quantity,precision))

                    #     bot.sendMessage(1039725953,'order confirmed')

                    # if 'SLS' in message[0]:
                    #     stock=str(message[1])
                    #     price=str(message[2])

                    #     for client in name:
                    #         data=client.get_account_snapshot(type='SPOT')
                    #         wallet=data['snapshotVos'][0]['data']['balances']
                    #         for i in wallet:
                    #             if i['asset']=='USDT':
                    #                 print(i)
                    #                 p_l=i['free']
                    #                 break

                    #         quantity=(((float(values[0]))/100) * p_l)/float(price)

                    #         quantity=float(quantity)
                    #         precision=int(get_precision(str(stock)))

                    #         order = client.create_order(
                    #             symbol=str(stock),
                    #             side=Client.SIDE_SELL,
                    #             type=Client.ORDER_TYPE_LIMIT,
                    #             price=str(price),
                    #             timeInForce='GTC',
                    #             quantity=round(quantity,precision))
                    #     bot.sendMessage(1039725953,'order confirmed')

                    # if 'SMB' in message[0]:
                    #     stock=str(message[1])
                    #     ltp=ltp_price(str(stock))

                    #     for client in name:
                    #         data=client.get_account_snapshot(type='SPOT')
                    #         wallet=data['snapshotVos'][0]['data']['balances']
                    #         for i in wallet:
                    #             if i['asset']=='USDT':
                    #                 print(i)
                    #                 p_l=i['free']
                    #                 break

                    #         quantity=(((float(values[0]))/100) * p_l)/float(ltp)

                    #         quantity=float(quantity)
                    #         precision=int(get_precision(str(stock)))

                    #         order = client.futures_create_order(
                    #             symbol=str(stock),
                    #             side=Client.SIDE_BUY,
                    #             type=Client.ORDER_TYPE_MARKET,

                    #             quantity=round(quantity,precision))

                    #     bot.sendMessage(1039725953,'order confirmed')

                    # if 'SMS' in message[0]:
                    #     stock=str(message[1])
                    #     ltp=ltp_price(str(stock))

                    #     for client in name:
                    #         data=client.get_account_snapshot(type='SPOT')
                    #         wallet=data['snapshotVos'][0]['data']['balances']
                    #         for i in wallet:
                    #             if i['asset']=='USDT':
                    #                 print(i)
                    #                 p_l=i['free']
                    #                 break

                    #         quantity=(((float(values[0]))/100) * p_l)/float(ltp)

                    #         quantity=float(quantity)
                    #         precision=int(get_precision(str(stock)))

                    #         order = client.futures_create_order(
                    #             symbol=str(stock),
                    #             side=Client.SIDE_SELL,
                    #             type=Client.ORDER_TYPE_MARKET,
                    #             quantity=round(quantity,precision))

                    #     bot.sendMessage(1039725953,'order confirmed')
    ##########SPOT#######################################################################
    ##########SPOT#######################################################################
    ##########SPOT#######################################################################
    ##########SPOT#######################################################################

                    if message[0] == 'CLOSE':
                        stock = message[1]

                        for client in name:
                            orders1 = client.futures_position_information()

                            for order in orders1:
                                if order['symbol'] == str(stock):
                                    try:
                                        print(order)
                                        if (float(order['positionAmt']))*1000 < 0:
                                            order1 = client.futures_create_order(
                                                symbol=str(order['symbol']),
                                                side=Client.SIDE_BUY,
                                                type=Client.ORDER_TYPE_MARKET,
                                                quantity=abs(float(order['positionAmt'])))

                                        if (float(order['positionAmt']))*1000 > 0:
                                            order1 = client.futures_create_order(
                                                symbol=str(order['symbol']),
                                                side=Client.SIDE_SELL,
                                                type=Client.ORDER_TYPE_MARKET,
                                                quantity=abs(float(order['positionAmt'])))

                                    except Exception as e:
                                        bot.sendMessage(1039725953, str(
                                            traceback.format_exc()))

                        for order in orders:
                            if order['symbol'] == stock:
                                orders.remove(order)
                                break
                        if value == 'account1':
                            bot.sendMessage(
                                1039725953, f'Position closed manually for {stock}')

            j = len(response)
        except Exception as e:
            bot.sendMessage(1039725953, str(traceback.format_exc()))


# %%

def f(name, value, orders, dictionary):

    df3 = pd.read_csv("parameters.csv")
    values = df3[str(value)]
    print(values)
    if value == 'account1':
        time.sleep(1)

    if value == 'account2':
        time.sleep(2)

    if value == 'account3':
        time.sleep(3)

    main(name, values, orders, value, dictionary)
    print(name)
# %%


info = client.futures_exchange_info()
orders = []
Processes = []
if __name__ == '__main__':

    Processes.append(Process(target=f, args=(
        account1, 'account1', orders, dictionary)))
    Processes.append(Process(target=f, args=(
        account2, 'account2', orders, dictionary)))
    Processes.append(Process(target=f, args=(
        account3, 'account3', orders, dictionary)))
    Processes.append(Process(target=f, args=(
        account4, 'account4', orders, dictionary)))


for process in Processes:
    process.start()


for process in Processes:
    process.join()

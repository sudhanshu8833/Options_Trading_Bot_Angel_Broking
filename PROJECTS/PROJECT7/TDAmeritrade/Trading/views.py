import json
import numpy as np
import pytz
import datetime
import requests
import websocket
import threading
import random
from urllib.parse import urlencode
import backtrader as bt
import tulipy
import time
import json

from django.contrib import messages
from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.decorators import login_required


from Trading.models import *
from Trading.models import Account
from Trading.models import Bot
from Trading.models import Strategy
from Trading.models import Order
from Trading.TDA import *
from Trading.TradingBot import *
from ta.volatility import *
from ta.trend import *
from ta.momentum import *




def dashboard(request):
    template = loader.get_template('pages/dashboard.html')
    context = {}
    return HttpResponse(template.render(context, request))

def login(request):
    template = loader.get_template('pages/login.html')
    context = {}
    return HttpResponse(template.render(context, request))

def login_account(request):
    if request.method == "POST":
        name = request.POST['name']
        pwd = request.POST['password']
        try:
            user = User.objects.filter(name=name, password=pwd).values()[0]
        except:
            template = loader.get_template('pages/login.html')
            context = {'login_error': "Username and Password are incorrect"}
            return HttpResponse(template.render(context, request))

        if user['permission'] == "admin":
            request.session['permission'] = "admin"
            request.session['user_id'] = user['id']
            return redirect('trading')

def trading(request):
    try:
        user_id = request.session['user_id']
        user = User.objects.filter(id=user_id).values()[0]
        api_key = user["td_consumer_key"]
        refresh_token = user["td_refresh_token"]
        if api_key == "" or refresh_token == "" or not check_td_account(refresh_token, api_key):
            messages.warning(request, "Your TD Account are not activated. Please check Refresh token and Consumer Key.")
            return redirect("account")
        '''
        if str(user_id) not in TD_BOT:
            user_info = Account.objects.filter(id=user_id).values()[0]
            td_refresh_token = user_info['td_refresh_token']
            td_consumer_key = user_info['td_consumer_key']
            if check_td_account(td_refresh_token, td_consumer_key):
                bot_list = Bot.objects.filter(user_id=user_id).values()
                if bot_list != []:
                    for item1 in bot_list:
                        if item1['status'] == True:
                            #threading.Thread(target=check_trading_account, args=(user_id,)).start()
                            threading.Thread(target=run_bot, args=(user_id, td_refresh_token, td_consumer_key,)).start()
                            # new_thread = threading.Thread(target=run_bot, args=(user_id, td_refresh_token, td_consumer_key,))
                            # TD_BOT[str(user_id)] = {"main_thread": new_thread, "td": TD(refresh_token=td_refresh_token, client_id=td_consumer_key)}
                            # new_thread.setDaemon(True)
                            # new_thread.start()
                            break


            else:
                messages.warning(request, "Your TD account are not activated. Please check account.")
        live_bot_list = Bot.objects.filter(user_id=user_id, type="live") .values()
        paper_bot_list = Bot.objects.filter(user_id=user_id, type="paper") .values()
        strategy_list = Strategy.objects.filter(user_id=user_id).values()
        template = loader.get_template('pages/trading.html')
        context = {
            "live_bot_list": live_bot_list,
            "paper_bot_list": paper_bot_list,
            "strategy_list": strategy_list
        }
        '''
        bot_list = []
        bot_temp = Bot.objects.filter(user=User.objects.get(id=request.session["user_id"])).values()
        entry_strategy_1 = Strategy.objects.filter(user=User.objects.get(id=request.session["user_id"]), part="1", position="Entry").values()
        entry_strategy_2 = Strategy.objects.filter(user=User.objects.get(id=request.session["user_id"]), part="2", position="Entry").values()
        entry_strategy_3 = Strategy.objects.filter(user=User.objects.get(id=request.session["user_id"]), part="3", position="Entry").values()
        close_strategy_1 = Strategy.objects.filter(user=User.objects.get(id=request.session["user_id"]), part="1", position="Close").values()
        close_strategy_2 = Strategy.objects.filter(user=User.objects.get(id=request.session["user_id"]), part="2", position="Close").values()
        close_strategy_3 = Strategy.objects.filter(user=User.objects.get(id=request.session["user_id"]), part="3", position="Close").values()
        template = loader.get_template('pages/trading.html')

        for bot in bot_temp:
            temp1 = json.loads(bot["entry"])
            bot["entry"] = ', '.join([Strategy.objects.get(id=item).name for item in temp1])
            temp2 = json.loads(bot["close"])
            bot["close"] = ', '.join([Strategy.objects.get(id=item).name for item in temp2])
        context = {
            "bot_list": bot_temp,
            "entry_strategy_1": entry_strategy_1,
            "entry_strategy_2": entry_strategy_2,
            "entry_strategy_3": entry_strategy_3,
            "close_strategy_1": close_strategy_1,
            "close_strategy_2": close_strategy_2,
            "close_strategy_3": close_strategy_3,
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print(e)
        request.session.flush()
        template = loader.get_template('pages/login.html')
        context = {'login_error': "You have no permission to connect this link."}
        return HttpResponse(template.render(context, request))

def strategy(request):
    try:
        result = []
        user_id = request.session['user_id']
        temp = Strategy.objects.filter(user_id=user_id).values()
        for item in temp:
            temp1 = json.loads(item["content"])
            # temp2 = '<br/>'.join([item1["indicator1"] + item1["period1"] + " Cross{} ".format(item1["condition"].title()) + item1["indicator2"] + item1["period2"] + " on {} Timeframe".format(item1["timeframe"].upper()) for item1 in temp1])
            temp2 = content_intepreter(temp1, item["part"], item["position"])

            result.append({
                "id": item["id"],
                "name": item["name"],
                "part": item["part"],
                "position": item["position"],
                "content": temp2
            })

        template = loader.get_template('pages/strategy.html')
        context = {
            "strategy_list": result
        }
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print(e)
        request.session.flush()
        template = loader.get_template('pages/login.html')
        context = {'login_error': "You have no permission to connect this link."}
        return HttpResponse(template.render(context, request))

def backtest(request):
    try:
        user_id = request.session['user_id']
        user = User.objects.filter(id=user_id).values()[0]
        api_key = user["td_consumer_key"]
        refresh_token = user["td_refresh_token"]
        if api_key == "" or refresh_token == "" or not check_td_account(refresh_token, api_key):
            messages.warning(request, "Your TD Account are not activated. Please check Refresh token and Consumer Key.")
            return redirect("account")
        bot_list = Bot.objects.filter(user_id=user_id).values()

        template = loader.get_template('pages/backtest.html')
        context = {
            "bot_list": bot_list,
        }
        return HttpResponse(template.render(context, request))

    except Exception as e:
        print(e)
        request.session.flush()
        template = loader.get_template('pages/login.html')
        context = {'login_error': "You have no permission to connect this link."}
        return HttpResponse(template.render(context, request))

def account(request):
    user_id = request.session["user_id"]
    account_info = User.objects.filter(id=user_id).values()[0]
    template = loader.get_template('pages/account.html')
    context = {
        "account_info": account_info
    }
    return HttpResponse(template.render(context, request))


@require_POST
def add_strategy(request):
    part = request.POST["part"]
    position = request.POST["position"]
    name = request.POST["name"]
    content = request.POST["content"]
    new_strategy = Strategy(part=part, position=position, name=name, content=content, user=User.objects.get(id=request.session["user_id"]))
    new_strategy.save()
    messages.success(request, "Success adding new strategy.")
    return JsonResponse({"result": "success"})

@require_POST
def add_bot(request):
    try:
        type = request.POST["type"]
        side = request.POST["side"]
        name = request.POST["name"]
        symbol = request.POST["symbol"]
        amount = float(request.POST["amount"])
        entry_strategy = request.POST["entry_strategy"]
        close_strategy = request.POST["close_strategy"]

        new_bot = Bot(user=User.objects.get(id=request.session["user_id"]), type=type, side=side, name=name, symbol=symbol, amount=amount, entry=entry_strategy, close=close_strategy)
        new_bot.save()

        return redirect("trading")
    except Exception as e:
        print(e)
        request.session.flush()
        template = loader.get_template('pages/login.html')
        context = {'login_error': "You have no permission to connect this link."}
        return HttpResponse(template.render(context, request))

@require_POST
def update_broker_info(request):
    try:
        user_id = request.session['user_id']
        refresh_token = request.POST['refresh_token']
        consumer_key = request.POST['consumer_key']
        User.objects.filter(id=user_id).update(td_refresh_token=refresh_token, td_consumer_key=consumer_key)
        messages.success(request, "Update TD Ameritrade account information successfully.")
        context = {
            "result": "success"
        }
        return JsonResponse(context)
    except Exception as e:
        print(e)
        request.session.flush()
        template = loader.get_template('pages/login.html')
        context = {'login_error': "There is an error in updating TD Account info."}
        return HttpResponse(template.render(context, request))

def delete_strategy(request, id):
    try:
        #Bot.objects.filter(user_id=user_id, strategy=id).delete()
        user_id = request.session['user_id']
        if check_strategy_in_bot(id):
            Strategy.objects.filter(user_id=user_id, id=id).delete()
            messages.success(request, "Delete strategy successfully")
        else:
            messages.warning(request, "This strategy is used in some bot so you can't delete this strategy. You can delete strategy when nothing bot use that.")
        return redirect("strategy")
    except Exception as e:
        print(e)
        messages.warning(request, "There is an issue in deleting strategy.")
        return redirect('strategy')

def check_strategy_in_bot(id):
    for bot in Bot.objects.all().values():
        if id in json.loads(bot["entry"]) or id in json.loads(bot["close"]):
            return False
    return True

@require_POST
def run_backtest(request):
    try:
        user_id = request.session["user_id"]
        #refresh_token = User.objects.get(id=user_id).td_refresh_token
        #consumer_key = User.objects.get(id=user_id).td_consumer_key
        bot_id = request.POST["bot_id"]
        #time_from = (datetime.datetime.strptime(request.POST["time_from"], "%Y-%m-%d") - datetime.datetime(1970, 1, 1)) // datetime.timedelta(milliseconds=1)
        #time_to = (datetime.datetime.strptime(request.POST["time_to"], "%Y-%m-%d") - datetime.datetime(1970, 1, 1)) // datetime.timedelta(milliseconds=1)

        time_from = int(datetime.datetime.strptime(request.POST["time_from"], "%Y-%m-%d").timestamp() * 1000)
        time_to = int(datetime.datetime.strptime(request.POST["time_to"], "%Y-%m-%d").timestamp() * 1000)
        TDB = TDBOT(user_id, bot_id)
        #TDB.get_history_data(time_from, time_to)
        #print(TDB.history_data)
        #print(TDB.time_frame)
        #print(TDB.strategy)
        if TDB.run_backtest(time_from, time_to):
            #print("success backtest")
            #print(TDB.history_data["15m"])
            #np.savetxt(r'one_data.txt', TDB.history_data["15m"].values, fmt='%s')
            chart_data = convert_to_chart(TDB.chart_data)
            #print(chart_data)
            #print(TDB.buy_signal)
            #print(TDB.sell_signal)
            #print(TDB.total_signal)
            win_count = 0
            lose_count = 0
            win_value = 0
            lose_value = 0
            result = 0.0
            for item in TDB.total_signal:
                if item["p_l"] != "":
                    if item["p_l"] > 0:
                        win_count += 1
                        win_value += item["p_l"]
                    elif item["p_l"] < 0:
                        lose_count += 1
                        lose_value += item["p_l"]
                    result += item["p_l"]
            #print("new value", win_count, lose_count, result)
            context = {
                "result": "success",
                "symbol": TDB.bot.symbol,
                "backtesting_result": TDB.total_signal,#trading_result,
                "buy_result": TDB.buy_signal,
                "sell_result": TDB.sell_signal,
                "main_time_frame": TDB.main_time_frame,
                "time_frame": TDB.time_frame,
                "chart_data": chart_data,
                "win_count": win_count,
                "lose_count": lose_count,
                "win_value": "%.4f" % win_value,
                "lose_value": "%.4f" % lose_value,
                "total_value": "%.4f" % result
            }
        else:
            context = {
                "result": "fail"
            }
            messages.warning(request, "There is a error in backtesting. Please ask this to administrator.")

        '''
        symbol = Bot.objects.get(id=bot_id).symbol
        entry_strategy_temp = json.loads(Bot.objects.get(id=bot_id).entry)
        close_strategy_temp = json.loads(Bot.objects.get(id=bot_id).close)
        entry_strategy = []
        close_strategy = []
        for item in entry_strategy_temp:
            entry_strategy.append(json.loads(Strategy.objects.get(id=item).content))
        for item in close_strategy_temp:
            close_strategy.append(json.loads(Strategy.objects.get(id=item).content))
        print(entry_strategy, close_strategy)
        time_from = (datetime.datetime.strptime(request.POST["time_from"], "%Y-%m-%d") - datetime.datetime(1970, 1, 1)) // datetime.timedelta(milliseconds=1)
        time_to = (datetime.datetime.strptime(request.POST["time_to"], "%Y-%m-%d") - datetime.datetime(1970, 1, 1)) // datetime.timedelta(milliseconds=1)
        history_data_original = TDA(refresh_token=refresh_token, client_id=consumer_key).get_history_data(symbol=symbol, start_time=time_from, end_time=time_to, frequency=1)
        history_data = history_data_original.rename(columns={"datetime": "x"})
        history_data["color"] = np.where(history_data["open"] <= history_data["close"], "#1b5e20", "#f44455")
        print(len(history_data))
        history_data['RSI'] = RSIIndicator(history_data['close'], window=14, fillna=True).rsi().astype('int32')
        color_list = []
        for index, row in history_data.iterrows():
            if row.open >= row.close:
                color_list.append("#f44455")
            else:
                color_list.append("#0cc2aa")
        temp1 = history_data.drop(columns={'RSI'})
        temp2 = history_data.drop(columns=['open', 'high', 'low', 'close', 'color'])
        candle_data = temp1.to_dict('records')
        rsi_data = temp2.values.tolist()
        # print(RSIIndicator(history_data['close'], window=14, fillna=True).rsi().astype('int32'))
        # history_data = history_data.astype({'RSI': 'int32'}).dtypes
        # df[["a", "b"]] = df[["a", "b"]].apply(pd.to_numeric)
        # history_data.apply
        # astype({'col1': 'int32'}).dtypes
        # print(history_data)
        # print(history_data.to_dict('records'))

        ##print(history_data)
        # temp1 = history_data
        # temp2 = history_data

        # del temp2['open']
        # del temp2['high']
        # del temp2['low']
        # print(temp1)

        # print(temp2)
        # candle_data = history_data.to_dict('records')#[]

        # candle_data = candle_data[14:]

        # print(len(candle_data))
        # print(candle_data)
        # print(rsi_data)
        # for index, row in history_data.iterrows():
        #    if row.open >= row.close:
        #        candle_data.append({"x": int(row.datetime), "open": row.open, "high": row.high, "low": row.low, "close": row.close, "color": "#f44455"})
        #    else:
        #        candle_data.append({"x": int(row.datetime), "open": row.open, "high": row.high, "low": row.low, "close": row.close, "color": "#0cc2aa"})
        # print(candle_data)
        # date_list = history_data['datetime'].to_list()
        # print(candle_data)
        close_list = history_data['close'].to_list()
        # print(close_list)
        # rsi_list = list(tulipy.rsi(np.array(close_list), 14))
        # print(len(rsi_list))
        # temp = RSIIndicator(history_data['close'], window=14, fillna=True)
        # print(temp.rsi())
        # print(temp)
        # print(np.round(rsi_list, 2))

        context = {
            # "hist_data": history_data
            "result": "success",
            "chart_data": candle_data,
            "rsi": rsi_data
        }
        '''

        return JsonResponse(context)
    except Exception as e:
        print(e)
        request.session.flush()
        context = {
            "result": "fail"
        }
        return JsonResponse(context)


def content_intepreter(content, part, position):
    try:
        if position == "Entry":
            if part == "1":
                return [item1["indicator1"] + item1["period1"] + " {} ".format(item1["condition1"].title()) + item1["indicator2"] + item1["period2"] + " on {} Timeframe".format(item1["timeframe"].upper()) for item1 in content]
            elif part == "2":
                time_frame = ', '.join(content["timeframe"]).upper()
                condition = [item1["indicator1"] + item1["period1"] + " {} ".format(item1["condition1"].title()) + item1["indicator2"] + item1["period2"] for item1 in content["content"]]
                return {
                    "timeframe": time_frame,
                    "condition": condition
                }
            elif part == "3":
                return [item1["indicator1"] + item1["period1"] + " {} ".format(item1["condition1"].title()) + item1["indicator2"] + item1["period2"] + " {} ".format(item1["operator1"]) + item1["indicator3"] + item1["period3"] + " {} ".format(item1["condition2"].title()) + item1["indicator4"] + item1["period4"] + " on {} Timeframe".format(item1["timeframe"].upper()) for item1 in content]
        elif position == "Close":
            result = []
            if part == "1":
                for item1 in content:
                    temp = item1["indicator1"] + item1["period1"] + " {} ".format(item1["condition1"].title()) + item1["indicator2"] + item1["period2"]
                    if item1["indicator3"] != "" and item1["period3"] != "" and item1["indicator4"] != "" and item1["period4"] != "":
                        temp += " {} ".format(item1["operator1"]) + item1["indicator3"] + item1["period3"] + " {} ".format(item1["condition2"].title()) + item1["indicator4"] + item1["period4"]
                    if item1["indicator5"] != "" and item1["period5"] != "" and item1["indicator6"] != "" and item1["period6"] != "":
                        temp += " {} ".format(item1["operator2"]) + item1["indicator5"] + item1["period5"] + " {} ".format(item1["condition3"].title()) + item1["indicator6"] + item1["period6"]
                    temp += " on {} Timeframe".format(item1["timeframe"])
                    result.append(temp)
                    '''
                    if item1["indicator5"] == "" or item1["period5"] == "" or item1["indicator6"] == "" or item1["period6"] == "":
                        result.append(item1["indicator1"] + item1["period1"] + " {} ".format(item1["condition1"].title()) + item1["indicator2"] + item1["period2"] + " {} ".format(item1["operator1"]) + item1["indicator3"] + item1["period3"] + " {} ".format(item1["condition2"].title()) + item1["indicator4"] + item1["period4"] + " on {} Timeframe".format(item1["timeframe"].upper()))
                    else:
                        result.append(item1["indicator1"] + item1["period1"] + " {} ".format(item1["condition1"].title()) + item1["indicator2"] + item1["period2"] + " {} ".format(item1["operator1"])
                                      + item1["indicator3"] + item1["period3"] + " {} ".format(item1["condition2"].title()) + item1["indicator4"] + item1["period4"] + " {} ".format(item1["operator2"])
                                      + item1["indicator5"] + item1["period5"] + " {} ".format(item1["condition3"].title()) + item1["indicator6"] + item1["period6"] + " on {} Timeframe".format(item1["timeframe"].upper()))
                    '''
                return result
            elif part == "2":
                time_frame = ', '.join(content["timeframe"]).upper()
                condition = [item1["indicator1"] + item1["period1"] + " {} ".format(item1["condition1"].title()) + item1["indicator2"] + item1["period2"] for item1 in content["content"]]
                return {
                    "timeframe": time_frame,
                    "condition": condition
                }
            elif part == "3":
                return [item1["indicator1"] + item1["period1"] + " {} ".format(item1["condition1"].title()) + item1["indicator2"] + item1["period2"] + " {} ".format(item1["operator1"]) + item1["indicator3"] + item1["period3"] + " {} ".format(item1["condition2"].title()) + item1["indicator4"] + item1["period4"] + " on {} Timeframe".format(item1["timeframe"].upper()) for item1 in content]
    except Exception as e:
        print(e)


def convert_to_chart(data):

    #for key, value in data.items():
    #    temp = value[["datetime", "open", "high", "low", "close"]]
    #    data[key] = temp.values.tolist()
    for key, value in data.items():
        result = []
        for index, row in value.iterrows():
            if row["open"] > row["close"]:
                result.append({"x": row["datetime"], "open": row["open"], "high": row["high"], "low": row["low"], "close": row["close"], "color": "#e91e63"})
            elif row["open"] < row["close"]:
                result.append({"x": row["datetime"], "open": row["open"], "high": row["high"], "low": row["low"], "close": row["close"], "color": "#4caf50"})
            else:
                result.append({"x": row["datetime"], "open": row["open"], "high": row["high"], "low": row["low"], "close": row["close"], "color": "#9e9e9e"})
        data[key] = result
    return data




def delete_bot(request, id):
    user_id = request.session['user_id']
    try:
        Bot.objects.filter(user_id=user_id, id=id).delete()
        messages.success(request, "Delete Bot successfully")
        return redirect("trading")
    except:
        messages.warning(request, "There is an issue in deleting bot.")
        return redirect('trading')

def update_bot_status(request):
    if request.method == "POST":
        user_id = request.session['user_id']
        id = request.POST['id']
        status = request.POST['status']
        if status == "0":
            Bot.objects.filter(id=id).update(status=False)
        elif status == "1":
            Bot.objects.filter(id=id).update(status=True)
            print(TD_BOT)
            if str(user_id) not in TD_BOT:
                user_info = Account.objects.filter(id=user_id).values()[0]
                td_refresh_token = user_info['td_refresh_token']
                td_consumer_key = user_info['td_consumer_key']
                threading.Thread(target=run_bot, args=(user_id, td_refresh_token, td_consumer_key,)).start()
            else:
                temp_symbol = []
                td_symbol = TD_BOT[str(user_id)]['symbol'].split(",")
                #bot_symbol = Bot.objects.filter(id=id).values()[0]['symbol'].split(",")
                #for symbol in bot_symbol:
                #    if symbol not in td_symbol:
                #        temp_symbol.append(symbol)
                #        td_symbol.append(symbol)
                bot_symbol = Bot.objects.filter(id=id).values()[0]['symbol']
                if bot_symbol not in td_symbol:
                    td_symbol.append(bot_symbol)
                    TD_BOT[str(user_id)]["symbol"] = ",".join(td_symbol)
                    auth_id = random.randint(1000, 9999)
                    '''params = {
                        "service": "CHART_EQUITY",
                        "requestid": auth_id,
                        "command": "SUBS",
                        "account": TD_BOT[str(user_id)]['td'].principal['accounts'][0]['accountId'],
                        "source": TD_BOT[str(user_id)]['td'].principal['streamerInfo']['appId'],
                        "parameters": {
                            # "keys": "DVAX,UNFI,DS,ABUS,COTY",
                            # "keys": ",".join(temp_symbol),  # "AAPL",
                            "keys": bot_symbol,
                            "fields": "0,1,2,3,4,5,6,7,8"
                        }
                    }'''
                    params = {
                        "service": "QUOTE",
                        "requestid": auth_id,
                        "command": "SUBS",
                        "account": TD_BOT[str(user_id)]['td'].principal['accounts'][0]['accountId'],
                        "source": TD_BOT[str(user_id)]['td'].principal['streamerInfo']['appId'],
                        "parameters": {
                            #"keys": self.symbol,
                            "keys": bot_symbol,
                            "fields": "0,1,2,3,4,5,6,7,8"
                        }
                    }
                    print(TD_BOT[str(user_id)])
                    TD_BOT[str(user_id)]['td'].ws.send(json.dumps(params))
                #print(td_symbol)
                #print(temp_symbol)
                TD_BOT[str(user_id)]["status"] = "run"

        context = {}
        return JsonResponse(context)

'''
def add_strategy(request):
    if request.method == "POST":
        user_id = request.session['user_id']
        strategy = request.POST['strategy']
        if strategy == "dema_cross":
            strategy_name = request.POST['strategy_name']
            short_period = request.POST['dema_short_period']
            long_period = request.POST['dema_long_period']
            param = ','.join(["long={}".format(long_period), "short={}".format(short_period)])
            if Strategy.objects.filter(user_id=user_id, name=strategy_name).values():
                messages.warning(request, " Duplicated strategy name exist. Don't duplicate same strategy name")
                return redirect('strategy')
            new_strategy = Strategy(name=strategy_name, user_id=user_id, parameter=param, indicator=strategy)
            new_strategy.save()
            #strategy_info = Strategy.objects.filter(user_id=user_id, name=strategy_name).values()
            messages.success(request, "Add new strategy successfully")
            return redirect('strategy')
'''















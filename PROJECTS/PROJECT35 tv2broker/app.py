import json
from flask import Flask, request
import requests

# client = Client(api_key=config.API_KEY, api_secret=config.API_SECRET)

app = Flask(__name__)
WEBHOOK_PASSPHRASE = "2#__j7y/PZMC6_z9hsdfkdjsh&*(&8IV#VQ(VcUr-#T9Vpl74&gt;FO_"

API_KEY = 'PKACLQQROWAF065TBT4N'
SECRET_KEY = 'L9VnN8BNLaH1zUTcQ3jEJWA7dpHdWnraz99QuPDf'
BASE_URL = "https://paper-api.alpaca.markets"
# BASE_URL = "https://app.alpaca.markets"

ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}

@app.route('/')
def welcome():
    return "Why are you here? We are busy making money!"


@app.route('/webhook', methods=['POST'])
def webhook():
    print("webhook1")

# data = request.get_json()

    data = {}


    try:

        data = json.loads(request.data)

    except ValueError as ex:
        return {
        "code": "error",
        "message": "invalid request",
        "request": request.data
        }




    print(data)

    data1 = data


    if data['PASSPHRASE'] != WEBHOOK_PASSPHRASE:
        return {
        "code": "error",
        "message": "Nice try, invalid passphrase"
        }

    else:
        data = {
        "symbol": data['SYMBOL'].upper(),
        "qty": int(data['QTY']),
        "side": data['SIDE'].lower(),
        "type": "market",
        "time_in_force": "gtc",
        "order_class": "simple"
        # "take_profit": {
        # "limit_price": data['close'] * 1.05
        # },
        # "stop_loss": {
        # "stop_price": data['close'] * 0.98,
        # }
        }

    print(data)


    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    try:
        response = json.loads(r.content)
        print(response)

        if 'id' not in response or 'client_order_id' not in response:
            return {
            "code": "error",
            "message": "invalid response1",
            "response": response,
            "data": data1
            }



        return {
        'webhook_message': data,
        'id': response['id'],
        'client_order_id': response['client_order_id']
        }
    except ValueError as e:
        return {
        "code": "error",
        "message": "invalid response",
        "response": r.content
        }

print("start")
if __name__ == '__main__':
    app.run(debug=True)
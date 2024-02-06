import pandas as pd
import time
import traceback
from datetime import datetime
import logging
import json
# from finta import TA
# from wrappers import retry
import ccxt
import uuid
import requests
from functools import wraps




#CONFIGURATIONS
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger('dev_log')
error = logging.getLogger('error_log')
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
data={}
with open("datamanagement/helpful_scripts/background.json") as json_file:
    data=json.load(json_file)

print(data)
client = MongoClient(data['mongo_uri'], server_api=ServerApi('1'),connect=False,tlsCAFile=certifi.where())

database=client[data['database']]
admin=database['admin']
position=database['position']

if(len(list(admin.find()))<1):
    admin.insert_one({
        "api_key":"65a8e33d36c65900017502d2",
        "secret_key":"9930e424-ec27-4d87-a9a5-5db412af3c18",
        "investment":1000,
        "symbols":["BTC/USDT","ETH/USDT"],
        "status":True,
        "live":False,
        "EMA_1_period":"",
        "EMA_2_period":"",
        "time_frame":"5m",
        "stoploss":2,
        "takeprofit":2
    })

pos=position.find_one()
save_it=pos
pos['current_price']=100

position.update_one({"_id":save_it['_id']},{'$set':pos})
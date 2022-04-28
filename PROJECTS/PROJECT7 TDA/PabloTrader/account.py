import numpy as np
import pandas as pd
import datetime
import time
#from decimal import Decimal
import pandas as pd
import requests
from datetime import date,timedelta
#import simplejson as json
import os
#import inspect
from ACCOUNT_DETAIL import ACCOUNT_ID_STRING,  CLIENT_ID_STRING


CLIENT_ID = CLIENT_ID_STRING
API_KEY = CLIENT_ID+"@AMER.OAUTHAP"

ACCOUNT_ID = ACCOUNT_ID_STRING


#CLIENT_ID = "NNHN2F5JZ0RIFT2K0OPSOPWBE7R85Z8Z"
#API_KEY = CLIENT_ID+"@AMER.OAUTHAP"
#ACCOUNT_ID = "270221776"

#https://auth.tdameritrade.com/oauth?client_id=DEARSOURABH99%40AMER.OAUTHAP&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1

#data_folder = inspect.getfile(src.techlib).replace("techlib.py","")
data_folder = os.path.dirname(os.path.realpath('__file__'))
filename = "REFRESH_TOKEN"
filepath = os.path.join(data_folder, filename)
REFRESH_TOKEN = open(filepath,"r").read()


def get_access_token(refresh_token=REFRESH_TOKEN, client_id=CLIENT_ID):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = [
      ('grant_type', 'refresh_token'),
      ('refresh_token', refresh_token),
      ('access_type', ''),
      ('code', ''),
      ('client_id', client_id),
      ('redirect_uri', ''),
    ]
    #print(REFRESH_TOKEN)

    resp = requests.post('https://api.tdameritrade.com/v1/oauth2/token', headers=headers, data=data)
    if resp.status_code != 200:
        raise Exception('Could not authenticate!')
    return resp.json()['access_token']

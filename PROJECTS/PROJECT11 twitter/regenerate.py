# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import time
import requests
import json


# %%
api_key='JZDOD9V6SNWYJJST7GXIFOKA3G5K7VOY'
with open("refresh.json") as json_data_file:
    data2 = json.load(json_data_file)
refresh_token=data2['refresh_token']


# %%
times1=time.time()
url='https://api.tdameritrade.com/v1/oauth2/token'

payload={'grant_type':'refresh_token',
        'refresh_token':refresh_token,
        

        'client_id':api_key
}
authReply=requests.post(url,data=payload)
data1=authReply.json()
print(data1)
access_token=data1['access_token']



  
# Data to be written
dictionary ={
    "access_token":access_token,
    "refresh_token":refresh_token
}
  
# Serializing json 
json_object = json.dumps(dictionary, indent = 2)
  
# Writing to sample.json
with open("refresh.json", "w") as outfile:
    outfile.write(json_object)






# %%
while True:
        if time.time()>times1+1500:
                url='https://api.tdameritrade.com/v1/oauth2/token'

                payload={'grant_type':'refresh_token',
                        'refresh_token':refresh_token,
                        

                        'client_id':api_key
                }
                authReply=requests.post(url,data=payload)
                data=authReply.json()
                access_token=data['access_token']
                dictionary ={
                "access_token":access_token,
                "refresh_token":refresh_token
                }
                
                # Serializing json 
                json_object = json.dumps(dictionary, indent = 2)
                
                # Writing to sample.json
                with open("refresh.json", "w") as outfile:
                        outfile.write(json_object)
                times1=time.time()



from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import ssl
database="MT5"
import certifi
ca = certifi.where()
print(type(ca))
uri = "mongodb+srv://sudhanshus883:uWZLgUV61vMuWp8n@cluster0.sxyyewj.mongodb.net/?retryWrites=true&w=majority"
client1 = MongoClient(uri,tlsCAFile=ca,connect=False)

bot=client1[database]
admin=bot['Admin']


data={
        "live":True,
        "lot_size":1,
        "symbol":"EURUSD",
        "price":{
            "bid":1.01,
            "ask":1.02
        },
        "profits":{
            "day":1.02,
            "week":9.03,
            "month":27.04
        },
        "pattern":{
            "pattern1":True,
            "pattern2":True,
            "pattern3":False
        }
    }


admin.insert_one(data)
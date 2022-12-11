from smartapi import SmartConnect
from smartapi import SmartWebSocket

obj = SmartConnect(api_key='NuTmF22y')
data = obj.generateSession("Y99521", "abcd@1234")
refreshToken = data['data']['refreshToken']

data=obj.ltpData("NFO", 'BANKNIFTY01SEP2239000PE', "51697")['data']['ltp']
print(data)
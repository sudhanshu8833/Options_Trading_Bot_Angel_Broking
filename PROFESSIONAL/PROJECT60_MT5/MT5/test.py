import MetaTrader5 as mt
from datetime import datetime
mt.initialize()

login = 51575772
password= "T*RuTf8q"
server = "ICMarketsEU-Demo"
print(server)
print(mt.login(login,password,server))

print(mt.copy_rates_from("TSLA.NAS",mt.TIMEFRAME_D1,))

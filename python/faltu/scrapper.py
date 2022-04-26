import requests
from bs4 import BeautifulSoup as bs 


URL='https://www.nseindia.com/market-data/pre-open-market-cm-and-emerge-market'


soup=bs(requests.get(URL).text,'html.parser')
print(soup)
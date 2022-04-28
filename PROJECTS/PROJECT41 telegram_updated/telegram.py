import telepot
import pandas as pd
bot = telepot.Bot('1715056219:AAGxytb3U1gIt1vlVn8Jf5b4za3E1HPuOd4')
bot.getMe()
import requests
import time
import urllib


j=0

while True:
    try:
        from pprint import pprint
        response = bot.getUpdates()
    

        if len(response)>j:
            if 'document' in response[-1]['message']:
                
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

                if response[-1]['message']['document']['file_name'].upper()=='PARAMETERS.CSV':
                    file_id=response[-1]['message']['document']['file_id']
                
                    endpoint=r"https://api.telegram.org/bot1715056219:AAGxytb3U1gIt1vlVn8Jf5b4za3E1HPuOd4/getFile?file_id={}".format(file_id)
                    content=requests.get(url=endpoint)
                    content=content.json()
                
                    file_path=content['result']['file_path']
                    endpoint=r"https://api.telegram.org/file/bot1715056219:AAGxytb3U1gIt1vlVn8Jf5b4za3E1HPuOd4/{}".format(file_path)
                    req = requests.get(endpoint)
                    url_content = req.content
                    csv_file = open('parameters.csv', 'wb')
                
                    csv_file.write(url_content)
                    csv_file.close()
                
                    bot.sendDocument(1039725953, document=open('parameters.csv', 'rb'))
                    bot.sendDocument(1851811921, document=open('parameters.csv', 'rb'))
                    bot.sendMessage(1039725953,'please veriy if the parameters are updated or not')
                    bot.sendMessage(1851811921,'please veriy if the parameters are updated or not')

            else:

                message=response[-1]['message']['text']
                
                message=message.upper()
                # if message=='SEE STOCKS':
                    
                #     bot.sendDocument(1039725953, document=open('stocks.csv', 'rb'))

                # if message=='CHANGE STOCKS':
                #     bot.sendMessage(1039725953,'please first write "SEE STOCKS" and have the list of presently running stocks and make all the changes you want and then send it back' )


                if message=='SEE PARAMETERS':
                    bot.sendDocument(1039725953, document=open('parameters.csv', 'rb'))
                    bot.sendDocument(1851811921, document=open('parameters.csv', 'rb'))

        j=len(response)

    except:
        print("some error")

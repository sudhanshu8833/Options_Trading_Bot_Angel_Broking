# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import tweepy
import webbrowser
import telepot
import requests
import json
import pandas as pd
bot = telepot.Bot('2045500207:AAG0pPe7z0cVnTiBXnJaL36iKEZ-zRag7AY')
bot.getMe()
print(bot.getMe())
import time

API_KEY= "4lrbEPy9aKcGaV5Wj9yTycHNw"
API_SECRET_KEY="8dkvMsshNOVtCd4eaHUnGHRJ5JOQ0Wpzq6PHAJZxJISTcyHhZm"
BEARER_TOKEN="AAAAAAAAAAAAAAAAAAAAAN36TAEAAAAAlXlJfjZZ07rgnQq7fYLOAyuhtoU%3D861baHvt5o0mJK0pP2YNkgE4ED5WhxcdlRCRrHQ9GAPbIimHR9"
ACCESS_TOKEN='768195544904720384-7VLObGFCGGJBNOcS4DCkOOs1Pp7lmks'
ACCESS_SECRET_TOKEN='9fnlFtG5OcIjDnmWuXwwe7inTOPpXDXHOSUGQdyIu8hZH'
df3 = pd.read_csv("parameters.csv")
df3.set_index("parameters",inplace=True)
df1=df3.T



callback_uri='oob'
username=str(df1['user_name'][0])
expiry=str(df1['expiry'][0])
tolerance=float(df1['tolerance'][0])
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY,callback_uri)
user_pin_input=int(df1['user_pin'][0])
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
accountId=str(df1['account_id'][0])

api = tweepy.API(auth)
api=tweepy.API(auth)
#me=api.me()
#print(me.screen_name)

tweets = api.user_timeline(screen_name=username, 
                           # 200 is the maximum allowed count
                           count=200,
                           include_rts = False,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )



position=int(df1['position'][0])
l=0
j=0
def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def order():
    global accountId,stock,expiry,strike_price,tolerance,position
    print(strike_price)
    print(price)
    print(stock)
    print(position)
    print(call_put)
    print(tolerance)
    print(expiry)
    print(accountId)

    tickers=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    month=['01','02','03','04','05','06','07','08','09','10','11','12']
    for i in range(len(tickers)):
        if tickers[i] in data[-4]:
            expiry=str(month[i])+str(data[-4][:2])+str(data[-4][-2:])


    with open("refresh.json") as json_data_file:
        data2 = json.load(json_data_file)
    access_token=data2['access_token']

    endpoint=f'https://api.tdameritrade.com/v1/accounts/{accountId}/orders'

    header = {'Authorization':"Bearer {}".format(access_token),
                "Content-Type":"application/json"}


    payload={
        "complexOrderStrategyType": "NONE",
        "orderType": "LIMIT",
        "session": "NORMAL",
        "price": str(price),
        "duration": "DAY",
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
        {
            "instruction": "BUY_TO_OPEN",
            "quantity": int(position),
            "instrument": {
            "symbol": str(stock)+'_'+str(expiry)+str(call_put)+str(strike_price),
            "assetType": "OPTION"
            }
        }
        ]
    }

    content = requests.post(url = endpoint, json = payload, headers = header)



def market_order(twee):
    global stock, quantity, strike_price, price, call_put,j,l,accountId,position,data
    tweet=twee
    print('ordered')
    # tickers=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    # for ticker in tickers:
    #     if ticker in tweet:
    #         j=1
    #         break

    if j!=1 and 'C $' in tweet and 'SPY' not in tweet and 'SPX' not in tweet and 'QQQ' not in tweet and 'ALERT BOUGHT' in tweet and '/' not in tweet:
        # list=find(tweet,' ')

        # number=list[3]
        # if len(list)>4:
        #     number21=list[4]
        #     price=float(tweet[number+2:number21])
        #     price=(price+price*(tolerance/100))

        # else:
        #     price=float(tweet[number+2:])
        #     price=(price+price*(tolerance/100))

        data=tweet.split(' ')
        price=float(data[-1])
        price=(price+price*(tolerance/100))

        price1=round(price,0)
        price_mid=price-price1
        rem=(price_mid*100)%5
        add=(5-rem)/100
        price_final=price+add
        price_final
        price_final=round(price_final,2)
        price=price_final
        
        # number=find(tweet,' ')[1]
        # number1=find(tweet,' ')[2]
        stock=data[0][1:]

        if 'P' in data[-3]:
            call_put='P'

        if 'C' in data[-3]:
            call_put='C'


        strike_price=data[-3][:-1]
        
        # upto=tweet.find('C $')
        # value=float(tweet[strike+1:upto])
        # value=round(value,1)
        # print(value)
        # if value%1==0.5:
        #     strike_price=round(value,1)

        # else:
        #     strike_price=int(value)

        quantity=int(position/price)
        order()
        bot.sendMessage(1428378228, 'BOUGHT OLD')
        bot.sendMessage(1428378228,f'stock={stock} call quantity = {position} strike_price={strike_price} ltp={price}')






    elif j!=1 and 'P $' in tweet and 'SPY' not in tweet and 'SPX' not in tweet and 'QQQ' not in tweet and 'ALERT BOUGHT' in tweet and '/' not in tweet:
        # list=find(tweet,' ')
        # number=list[3]
        # if len(list)>4:
        #     number21=list[4]
        #     price=float(tweet[number+2:number21])
        #     price=(price+price*(tolerance/100))

        # else:
        #     price=float(tweet[number+2:])
        #     price=(price+price*(tolerance/100))
        data=tweet.split(' ')
        price=float(data[-1])
        price=(price+price*(tolerance/100))

        price1=round(price,0)
        price_mid=price-price1
        rem=(price_mid*100)%5
        add=(5-rem)/100
        price_final=price+add
        price_final
        price_final=round(price_final,2)
        price=price_final

        stock=data[0][1:]

        if 'P' in data[-3]:
            call_put='P'

        if 'C' in data[-3]:
            call_put='C'

        strike_price=data[-3][:-1]
        # upto=tweet.find('P $')
        # value=float(tweet[strike+1:upto])
        # value=round(value,1)
        # print(value)
        # if value%1==0.5:
        #     strike_price=round(value,1)

        # else:
        #     strike_price=int(value)
        quantity=int(position/price)

        order()
        bot.sendMessage(1428378228, 'BOUGHT OLD')
        bot.sendMessage(1428378228,f'stock={stock} put quantity = {position} strike_price={strike_price} ltp={price}')


twee='there are no tweets from this twitter handle'

while True:
    time.sleep(.69)
    for info in tweets[:3]:

        if l>0:
            # print("ID: {}".format(info.id))
            # print(info.created_at)
            twee=info.full_text
            print(twee)
            if twee!=previous_tweet:
                market_order(twee)
            break

        if l==0:
            # print("ID: {}".format(info.id))
            # print(info.created_at)
            
            twee=info.full_text    
            print(twee)
            l=1  
            break     
    tweets = api.user_timeline(screen_name=username, 
                           # 200 is the maximum allowed count
                           count=200,
                           include_rts = False,
                           # Necessary to keep full_text 
                           # otherwise only the first 140 words are extracted
                           tweet_mode = 'extended'
                           )

    previous_tweet=twee
    print('################################################################################################')


# %%




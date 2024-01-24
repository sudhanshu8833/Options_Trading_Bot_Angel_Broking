import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
zones=[]


'''
{
    "start_time":"",
    "price_low":100,
    "price_high":110
}

'''

class Zoning():

    def __init__(self,instrument):
        self.instrument=instrument
        self.download()
        self.zones=[]
        self.accumulator=30
        self.pip_size=.01


    def download(self):
        now = datetime.now()
        midnight_today = now.replace(hour=0, minute=0, second=0, microsecond=0)

        self.df=yf.download(self.instrument,interval="5m",start=midnight_today,end=datetime.now())
        self.df_1h=yf.download(self.instrument,interval="1h",start=midnight_today,end=datetime.now())

    def is_5SR_peak(self,index):
        
        points=0

        if(self.df.Close.iloc[index-2]>self.df.Close.iloc[index-3]):
            if(self.df.Close.iloc[index-2]>self.df.Open.iloc[index-2]):
                if(self.df.Close.iloc[index-2]>self.df.Open.iloc[index-3]):
                    if(self.df.Close.iloc[index-2]>self.df.Close.iloc[index-1]):
                        if(self.df.Close.iloc[index-2]>self.df.Open.iloc[index]):
                            if(self.df.Close.iloc[index-1]<self.df.Open.iloc[index-1]):
                                if(self.df.Close.iloc[index-2]>self.df.Close.iloc[index-4]):
                                    if(self.df.Close.iloc[index-2]>self.df.Close.iloc[index-5]):
                                        if(self.df.Close.iloc[index-2]>self.df.Open.iloc[index-1]):
                                            if(self.df.Close.iloc[index-2]>self.df.Close.iloc[index-6]):
                                                if(self.df.Close.iloc[index-2]>self.df.Open.iloc[index-3]):
                                                    if(self.df.Close.iloc[index-2]>self.df.Open.iloc[index-4]):
                                                        if(self.df.Close.iloc[index-2]>self.df.Open.iloc[index-5]):
                                                            points+=1

        if(self.df.Close.iloc[index-1]>self.df.Close.iloc[index] or self.df.Close.iloc[index]<self.df.Close.iloc[index-2]):
            points+=1
        
        if(self.df.Close.iloc[index-2]-self.df.Close.iloc[index-3]>=15*self.pip_size or self.df.Close.iloc[index-2]-self.df.Close.iloc[index-3]>=20*self.pip_size or self.df.Close.iloc[index-2]-self.df.Close.iloc[index-4]>=25*self.pip_size):
            points+=1
        
        if(points==3):
            return True
        
        return False



    def update_zones(self,index):


        if(self.is_5SR_peak(index)):
            price=self.df.Close.iloc[index]
            for zone in self.zones:
                if(abs(price-zone["price_high"])<=self.accumulator*self.pip_size or abs(price-zone['price_low'])<=self.accumulator*self.pip_size):
                    zone['price_high']=max(price,zone['price_high'])
                    zone['price_low']=min(price,zone['price_low'])
                    return
                    
            self.zones.append({
                "start_time":self.df.index[index],
                "price_high":self.df.Close.iloc[index],
                "price_low":self.df.Close.iloc[index],
                "type":"5minS+R"
            })

    def run(self):
        self.zones.append({
            "start_time":self.df.index[0],
            "price_high":self.df.High.iloc[0],
            "price_low":self.df.High.iloc[0],
            "type":"5minS+R"
        })

        self.zones.append({
            "start_time":self.df.index[0],
            "price_high":self.df.Low.iloc[0],
            "price_low":self.df.Low.iloc[0],
            "type":"5minS+R"
        })


        for i in range(6,len(self.df)):
            self.update_zones(i)


if __name__=="__main__":
    zone=Zoning("MNQ=F")
    zone.run()
    print(zone.zones)

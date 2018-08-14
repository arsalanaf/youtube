# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 15:13:26 2018

@author: Python Trading
"""

import keys
import datetime
from time import sleep
from binance.client import Client

client = Client(keys.APIKey, keys.SecretKey) 

symbol= 'BTCUSDT'
quantity= '0.05'

order= False
while order==False:
    BTC= client.get_historical_klines(symbol=symbol, interval='30m', start_str="1 hour ago UTC")
    if (float(BTC[-1][4])-float(BTC[-2][4]))>500:
        print ('Buyyy')
        client.order_market_buy(symbol= symbol, quantity= quantity)
        order= True
    elif (float(BTC[-1][4])-float(BTC[-2][4]))<-500:
        print ('Sellll')
        client.order_market_buy(symbol= symbol , quantity= quantity)
        order= True
    else:
        print ('Do nothing')
    sleep(10)
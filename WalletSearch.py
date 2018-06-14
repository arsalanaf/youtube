# -*- coding: utf-8 -*-
import pandas as pd
import requests
from time import sleep

richWallet=[]
dollars=[]
page=100

while page>20:
    page-=1
    sleep(5)
    url= 'https://bitinfocharts.com/top-100-richest-bitcoin-addresses-' + str(page)+ '.html'
    header = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
      "X-Requested-With": "XMLHttpRequest"
    }
    r = requests.get(url, headers=header)
    walletlist= pd.read_html(r.text, parse_dates=True)
    wallets= walletlist[1]
    try:
        wallets.columns= ['Number', 'Address', 'Balance', '% of coins', 'First In', 'Last In', 'Number Of Ins', 'First Out', 'Last Out', 'Number Of Outs' ]
        wallets['Number Of Outs'].dropna(how='all', inplace=True)
        traders=wallets[(wallets['Last Out']>'2018-01-01') & (wallets['Number Of Outs']>10)]
        for j in range(len(traders['Address'])):
                try:   
                    sleep(2)
                    urljoin= ('https://bitinfocharts.com/bitcoin/address/'+ traders['Address'].values[j]).split('wallet')[0]
                    url2= urljoin
                    r2 = requests.get(url2, headers=header)
                    wal1= pd.read_html(r2.text)
                except:
                    try:
                        url2= url2+'-full'
                        r2 = requests.get(url2, headers=header)
                        sleep(5)
                        wal1= pd.read_html(r2.text)
                        tr=wal1[2]
                        tr['Cash']= tr['Balance, USD'].apply(lambda x: x.split('@')[1]).replace('[$,]', '', regex=True).astype(float)
                        tr['Quantity']= tr['Amount'].replace('[BTC,]', '', regex=True).astype(float)
                        tr['Dollar']=-tr['Quantity']*tr['Cash']
                        profit= tr['Dollar'].sum()-(tr['Balance'].replace('[BTC,]', '', regex=True).astype(float)[0]*tr['Cash'][0])
                        print(profit)
                        if float(profit)>1000.00:
                            richWallet.append(urljoin)
                            dollars.append(profit)
                    except:
                        print('Failed')
    except:
        print ('Table Problem')

richTrader= pd.DataFrame({'URL Link': richWallet,
              'Profited': dollars
            }) 
richTrader.to_csv('List.csv')
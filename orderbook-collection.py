import time
import requests
import pandas as pd
import datetime

while(1):
    
   

    book = {}
    response = requests.get ('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    book = response.json()


    data = book['data']

    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids = bids.reset_index(); del bids['index']
    bids['type'] = 0
    
    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1 

    df = bids.append(asks)
    df['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df.to_csv("test.csv", index=False, header=False, mode = 'a')    
    print (df)

    # print (bids)
    print ("\n")
    # print (asks)

    time.sleep(1)
    continue;

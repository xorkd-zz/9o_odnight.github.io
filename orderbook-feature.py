import pandas as pd
import numpy as np 


df = pd.read_csv('2023-04-28-bitumb-btc-orderbook copy.csv').apply(pd.to_numeric,errors='ignore')
group_o = df.groupby(['timestamp'])


_timestamp = []
_mid_price = []
_mid_price_wt = []
_mid_price_mkt = []
_book_imbalance = []
_variance_of_order_size = []
for group_o, gr_o in group_o.groups.items():
        
    timestamp = df.loc[gr_o[0], "timestamp"]
    _timestamp.append (timestamp)
    
    # Basic of Midprice
    top_bid_price = df.loc[gr_o[0],"price"]
    top_ask_price = df.loc[gr_o[5], "price"]
    mid_price = (top_bid_price + top_ask_price) * 0.5
    _mid_price.append(mid_price)

    # Midprice for weignted
    i = 0
    Mean_bid_price = 0
    Mean_ask_price = 0
    while (i<5):
        Mean_bid_price += df.loc[gr_o[i],"price"]
        Mean_ask_price += df.loc[gr_o[i+5],"price"]
        i += 1
    mid_price_wt = (Mean_bid_price + Mean_ask_price) * 0.5
    _mid_price_wt.append (mid_price_wt)

    # Midprice for market
    top_bid_qty = df.loc[gr_o[0], "quantity"]
    top_ask_qty = df.loc[gr_o[5], "quantity"]
    mid_price_mkt = ((top_bid_price * top_ask_qty) + 
                     (top_ask_price * top_bid_qty)) / (top_bid_qty + top_ask_qty)
    _mid_price_mkt.append (mid_price_mkt)

    # Book Imbalance
    ratio = 0.2
    level = 5
    interval = 1
    askQty = 0
    bidQty = 0
    bidPx = 0
    askPx = 0
    j = 0
    while (j<5):
        bidQty += pow(df.loc[gr_o[j], "quantity"], ratio)
        askQty += pow(df.loc[gr_o[j+5], "quantity"], ratio)
        bidPx += df.loc[gr_o[j],"price"] * pow(df.loc[gr_o[j], "quantity"], ratio)
        askPx += df.loc[gr_o[j+5],"price"] * pow(df.loc[gr_o[j+5], "quantity"], ratio)
        j += 1
    book_price = (((askQty * bidPx)/bidQty) + ((bidQty * askPx) / askQty)) / (bidQty + askQty)
    book_imbalance = (book_price - mid_price) / interval
    _book_imbalance.append(book_imbalance)

    # Variance of Order Quantity = (Sum of order quantity - Mean order Quantity)^2 / total number of orders
    # Mean order quantity = Sum of Order Quantity / Total Number of Orders
    ordQty = 0 # sum of order Quantity
    ordNum = 10 # total number of orders
    k = 0
    while (k<5):
        ordQty += df.loc[gr_o[k], "quantity"] + df.loc[gr_o[k+5], "quantity"]
        k += 1
    mean_order_qty = ordQty / ordNum
    variance_of_order_size = pow((ordQty - mean_order_qty),2) / ordNum
    _variance_of_order_size.append(variance_of_order_size)
 


result = pd.DataFrame({'timestamp': _timestamp, 'mid_price': _mid_price,
                        'mid_price_wt': _mid_price_wt, 'mid_price_mkt': _mid_price_mkt, 
                        'book_imbalance-0.2-5-1': _book_imbalance, 'variance_of_order_size': _variance_of_order_size })
result.to_csv('result 2.csv', index=False)

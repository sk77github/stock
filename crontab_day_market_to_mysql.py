# -*-coding:utf-8 -*-

import sys
import time
import datetime
import tushare as ts
from sqlalchemy import create_engine

engine = create_engine('mysql://user:password@127.0.0.1/stock?charset=utf8')



all_stock_now_data = ts.get_today_all()

for value in all_stock_now_data.values:
    stock_code = value[0]
    print(stock_code)

    if stock_code in ['603228','300583','002838']:
       print('is new stock')
       continue

    data = ts.get_hist_data(stock_code,start="2017-01-06",end="2017-01-06")
    data['stock_code']=stock_code
    data.to_sql('market_data_day', engine, if_exists='append')


sys.exit()

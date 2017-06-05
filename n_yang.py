# -*-coding:utf-8 -*-

import sys
import time
import datetime
import pandas as pd
import tushare as ts
from sqlalchemy import create_engine

reload(sys)
sys.setdefaultencoding("utf-8")

engine = create_engine('mysql://user:password@127.0.0.1/stock?charset=utf8')


yang_num = int(sys.argv[1]) - 1
yang_num = str(yang_num)

sql = "select code,industry,timeToMarket,totals,reservedPerShare from stock_base_data_2016_3"
stock_base_data = pd.read_sql(sql, engine)

sql = "select avg(close) as db_close, stock_code as code from market_data_day where date in (select date from (select distinct date from market_data_day order by date desc limit 60) as t) group by stock_code"
stock_price_data = pd.read_sql(sql, engine)

all_stock_now_data = ts.get_today_all()
all_stock_now_data = all_stock_now_data[all_stock_now_data.trade > all_stock_now_data.open]
all_stock_now_data = all_stock_now_data[['volume', 'code','name','trade','changepercent']]
all_stock_now_data['volume'] =  all_stock_now_data['volume']/100

#two sub query because mysql version
sql = "select stock_code as code,count(distinct date),volume as db_volume,v_ma5,v_ma10 from market_data_day  where close > open and date in (select date from (select distinct date from market_data_day order by date desc limit " + yang_num + ") as t) group by stock_code having count(distinct date) = " + yang_num + " and db_volume > v_ma5 and db_volume > v_ma10"
stock_his_data = pd.read_sql(sql, engine)


all_stock_now_data = pd.merge(all_stock_now_data, stock_base_data, on='code')
all_stock_now_data = pd.merge(all_stock_now_data, stock_his_data, on='code')
all_stock_now_data = pd.merge(all_stock_now_data, stock_price_data, on='code')
all_stock_now_data = all_stock_now_data[all_stock_now_data.volume > all_stock_now_data.db_volume]
all_stock_now_data = all_stock_now_data[all_stock_now_data.trade > all_stock_now_data.db_close]
print(all_stock_now_data.sort(['totals'],ascending=True))

sys.exit()

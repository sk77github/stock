# -*-coding:utf-8 -*-

import sys
import time
import datetime
import numpy as np
import pandas as pd
import tushare as ts
from sqlalchemy import create_engine

reload(sys)
sys.setdefaultencoding("utf-8")


engine = create_engine('mysql://user:password@127.0.0.1/stock?charset=utf8')


num_day = int(sys.argv[1])

today = datetime.date.today()
select_date = today - datetime.timedelta(days=num_day)


sql = "select code,name,industry,pb,pe from stock_base_data_2016_3"
stock_base_data = pd.read_sql(sql, engine)


all_stock_now_data = ts.get_today_all()
all_stock_now_data = all_stock_now_data[['trade', 'code']]
all_stock_now_data = all_stock_now_data.set_index('code')

sql = "select close as trade, stock_code as code from market_data_day where date = \"" + str(select_date) +"\" group by stock_code"
stock_his_data = pd.read_sql(sql, engine)
stock_his_data = stock_his_data.set_index('code')

div_son = all_stock_now_data - stock_his_data
div_son_zhang = div_son[div_son.trade > 0]
div_son_die = div_son[div_son.trade < 0]
stock_high = (div_son_zhang/stock_his_data)*100
stock_high_die = (abs(div_son_die)/stock_his_data)*100
stock_high['code']=stock_high.index
stock_high_die['code']=stock_high_die.index

stock_high = pd.merge(stock_high, stock_base_data)
stock_high_die = pd.merge(stock_high_die, stock_base_data)
stock_high = stock_high.sort(['trade'],ascending=False)
stock_high_die = stock_high_die.sort(['trade'],ascending=False)
stock_high = stock_high[stock_high.trade < 100]
stock_high_die = stock_high_die[stock_high_die.trade < 100]
print(stock_high)
print("\n")
print("\n")
print(stock_high_die)
sys.exit()

if num_day == 1:
    stock_high = stock_high[stock_high.trade < 9.9]
elif num_day == 2:
    stock_high = stock_high[stock_high.trade < 20]
elif num_day == 3:
    stock_high = stock_high[stock_high.trade < 30]
print(stock_high)
print("\n")
print("\n")
sys.exit()

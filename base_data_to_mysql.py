# -*-coding:utf-8 -*-

import sys
import time
import datetime
import tushare as ts
from sqlalchemy import create_engine

engine = create_engine('mysql://user:password@127.0.0.1/stock?charset=utf8')




#stock_base = ts.get_stock_basics()
#stock_base.to_sql('stock_base_data_2016_3', engine, if_exists='append')
#sys.exit()

for i in range(1,5):
    for j in range(2005,2016):
        m = str(i)
        n = str(j)
        stock_growth = ts.get_growth_data(j,i)
        stock_growth.to_sql('stock_growth_data_'+n+'_'+m, engine, if_exists='append')
        stock_profit = ts.get_profit_data(j,i)
        stock_profit.to_sql('stock_profit_data_'+n+'_'+m, engine, if_exists='append')

#sys.exit()

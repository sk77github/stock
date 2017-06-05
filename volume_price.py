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


today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
yesterday_before = today - datetime.timedelta(days=2)
date_5 = today - datetime.timedelta(days=5)
date_60 = today - datetime.timedelta(days=60)



sql = "select code,industry,pb,pe,totals,reservedPerShare from stock_base_data_2016_3"
stock_base_data = pd.read_sql(sql, engine)

sql = "select code,roe,eps,net_profits,gross_profit_rate,net_profit_ratio from stock_profit_data_2016_3"
stock_profit_data = pd.read_sql(sql, engine)

sql = "select code,mbrg,nprg from stock_growth_data_2016_3"
stock_growth_data = pd.read_sql(sql, engine)


all_stock_now_data = ts.get_today_all()
#all_stock_now_data['volume'] = map(lambda x: x/100 , all_stock_now_data['volume'])
all_stock_now_data['volume'] =  all_stock_now_data['volume']/100

sql = "select max(volume) as db_volume, max(close) as db_close, stock_code as code from market_data_day where date between \"" + str(date_60) + "\" and \"" + str(yesterday) +"\" group by stock_code"
stock_his_data = pd.read_sql(sql, engine)

stock_trade_data_for_growth = pd.merge(all_stock_now_data, stock_base_data, on='code')
stock_trade_data_for_profit = pd.merge(stock_trade_data_for_growth, stock_growth_data, on='code')
stock_trade_data_for = pd.merge(stock_trade_data_for_profit, stock_profit_data, on='code')
stock_trade_data = pd.merge(stock_trade_data_for, stock_his_data, on='code')
stock_trade_data_volume = stock_trade_data[stock_trade_data.volume > stock_trade_data.db_volume]
stock_trade_data = stock_trade_data_volume[stock_trade_data_volume.trade > stock_trade_data_volume.db_close]
stock_trade_data = stock_trade_data[stock_trade_data.trade > stock_trade_data.open]
stock_trade = stock_trade_data[['code', 'name', 'trade', 'changepercent', 'industry', 'eps', 'roe','gross_profit_rate','mbrg','nprg','net_profits','totals']].sort(['totals'],ascending=True)
one = stock_trade[stock_trade.roe > 5]
#stock_trade = stock_trade[stock_trade.eps > 0.15]
#stock_trade = stock_trade[stock_trade.gross_profit_rate > 9]
#stock_trade = stock_trade[stock_trade.mbrg > 5]
#stock_trade = stock_trade[stock_trade.nprg > 5]
print(one)
two = stock_trade[stock_trade.roe < 5]
print(two)

sys.exit()

# Python量化交易代码
文件交易策略说明如下：

base_data_to_mysql.py
基本面数据录入MySQL数据库

crontab_day_market_to_mysql.py
每日行情数据录入MySQL数据库

datasource
一些数据源

high.py
根据输入参数N，选出近N天内涨幅最大，跌幅最大的股票并排序

n_yang.py
根据输入参数N，
选出近N天内K线连续为阳线
且量能大于5日，10日平均量能的股票

volume_price.py 
在当日K线为阳线的股票中，
选取行情量价高于一定日期内行情量价，
且上一季度财报
roe > 5
eps > 0.15
gross_profit_rate > 9
mbrg > 5
nprg > 5
按市值从小到大排序。


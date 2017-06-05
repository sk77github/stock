# Python量化交易代码
文件交易策略说明如下：

volume_price.py 
在当日为阳线的股票中，
选取行情量价高于一定日期内行情量价，
且上一季度财报
roe > 5
eps > 0.15
gross_profit_rate > 9
stock_trade.mbrg > 5
stock_trade.nprg > 5
按市值从小到大排序。


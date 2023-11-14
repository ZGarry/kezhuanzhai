"""
初始化qmt运行所需要的核心数据
"""

import time
from xtquant import xtdata
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount

from MyXtQuantTraderCallBack import MyXtQuantTraderCallback

xtdata.download_sector_data()

# 启动xt_trader
print("start")
# 指定客户端所在路径
path = r'C:\temp\soft\国金证券QMT交易端\userdata_mini'
# 生成session id 整数类型 同时运行的策略不能重复
session_id = int(time.time())
xt_trader = XtQuantTrader(path, session_id)
# 创建资金账号为 800068 的证券账号对象
acc = StockAccount('8880759259', 'STOCK')

# 创建交易回调类对象，并声明接收回调
callback = MyXtQuantTraderCallback()
xt_trader.register_callback(callback)

# 启动交易线程
xt_trader.start()

# 建立交易连接，返回0表示连接成功
connect_result = xt_trader.connect()
print('建立交易连接，返回0表示连接成功', connect_result)
# 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
subscribe_result = xt_trader.subscribe(acc)
print('对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功', subscribe_result)

"""
初始化qmt运行所需要的核心数据
"""

import time
from xtquant import xtdata
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount
from Settings import mini_qmt_path, account_id

from MyXtQuantTraderCallBack import MyXtQuantTraderCallback

init_flag = False
xt_trader = None
acc = None


def init():
    global xt_trader
    global acc
    xtdata.download_sector_data()

    # 启动xt_trader
    # 指定客户端所在路径
    path = mini_qmt_path
    # 生成session id 整数类型 同时运行的策略不能重复
    session_id = int(time.time())
    xt_trader = XtQuantTrader(path, session_id)
    # 创建资金账号为 800068 的证券账号对象
    acc = StockAccount(account_id, 'STOCK')

    # 创建交易回调类对象，并声明接收回调
    callback = MyXtQuantTraderCallback()
    xt_trader.register_callback(callback)

    # 启动交易线程
    xt_trader.start()

    # 建立交易连接，返回0表示连接成功
    connect_result = xt_trader.connect()
    if connect_result != 0:
        raise Exception("交易连接失败，程序终止")
    # 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
    subscribe_result = xt_trader.subscribe(acc)
    if subscribe_result != 0:
        raise Exception("交易回调订阅失败，程序终止")


try:
    init()
    init_flag = True
except:
    print("软件尚未启动或找不到位置")

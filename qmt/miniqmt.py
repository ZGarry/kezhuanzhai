# coding:utf-8

import time
import schedule
from MyPos import MyPos
from Settings import test_mode
from init import xt_trader, acc, init_flag
from qmt.datechecker.checkDebt import check_debt
from qmt.datechecker.DateChecker import registChecker
from qmt.dingding.XiaoHei import xiaohei
from util import today_is_trade_day

def daily_task():
    if not today_is_trade_day():
        xiaohei.send_text(f"今天非交易日，不进行交易")
        return

    # 股票信息展示（必须-同时获取股票信息）
    if init_flag:
        my.showMyPos()

    # 跑策略
    if init_flag:
        my.two_low()

    # 买逆回购，剩下的资金买逆回购
    if init_flag:
        my.buy_ni_hui_gou()

# 早安操作，做一些造成进行的内容
def good_morning():
    # 个人股票展示
    if init_flag:
        my.showMyPos()

    # 负债提醒
    check_debt()

    # 今天是否是交易日
    is_trade_day = today_is_trade_day()
    xiaohei.send_text(f"今天是否是交易日：{is_trade_day}")


my = MyPos(xt_trader, acc, init_flag)
# 日常事务检查
registChecker()

if test_mode:
    # 测试任务
    good_morning()
    daily_task()

else:
    # 早上好
    schedule.every().day.at("08:35").do(good_morning)
    # 正常买入
    schedule.every().day.at("13:35").do(daily_task)

    while True:
        schedule.run_pending()
        time.sleep(1)

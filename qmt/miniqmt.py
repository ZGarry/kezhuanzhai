# coding:utf-8

import time
import schedule
from MyPos import MyPos
from Settings import test_mode
from init import xt_trader, acc
from checkDebt import check_debt
from DateChecker import registChecker


def daily_task():
    # 负债提醒
    check_debt()

    # 股票信息展示（必须-同时获取股票信息）
    my.showMyPos()

    # 跑策略
    my.two_low()

    # 买逆回购，剩下的资金买逆回购
    my.buy_ni_hui_gou()


def good_morning():
    my.showMyPos()


my = MyPos(xt_trader, acc)
# 日常事务检查
registChecker()

daily_task()

# if test_mode:
#     # 测试任务
#     good_morning()
#     daily_task()

# else:
#     # 早上好
#     schedule.every().day.at("08:35").do(good_morning)
#     # 正常买入
#     schedule.every().day.at("09:41").do(daily_task)

#     while True:
#         schedule.run_pending()
#         time.sleep(1)

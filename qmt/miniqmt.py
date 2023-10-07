# coding:utf-8
from xtquant import xtconstant
from xtquant import xtdata
import pandas as pd

from qmt.MyPos import MyPos
from qmt.Settings import test_mode
from qmt.init import xt_trader, acc

import schedule
import time


def daily_task():
    my.showMyPos()
    my.f_Low()

def good_morning():
    my.showMyPos()


my = MyPos(xt_trader, acc)
# 每天的固定时间执行任务
if test_mode:
    # 测试任务
    good_morning()
    daily_task()
else:
    schedule.every().day.at("13:49").do(daily_task)

    # schedule.every().day.at("10:35").do(good_morning)
    while True:
        schedule.run_pending()
        time.sleep(1)


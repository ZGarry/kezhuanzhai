# coding:utf-8

import time

import schedule

from qmt.MyPos import MyPos
from qmt.Settings import test_mode
from qmt.init import xt_trader, acc


def daily_task():
    my.showMyPos()
    my.f_Low()


def good_morning():
    my.showMyPos()


my = MyPos(xt_trader, acc)
if test_mode:
    # 测试任务
    good_morning()
    daily_task()
else:
    # 早上好
    schedule.every().day.at("8:35").do(good_morning)
    # 正常买入
    schedule.every().day.at("13:19").do(daily_task)

    while True:
        schedule.run_pending()
        time.sleep(1)

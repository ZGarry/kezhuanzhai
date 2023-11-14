# coding:utf-8

import time

import schedule

from MyPos import MyPos
from Settings import test_mode
from init import xt_trader, acc
from checkDebt import check_debt
from DateChecker import registChecker

# 筛选出正股>50亿的


def daily_task():
    check_debt()

    my.showMyPos()
    my.f_Low()


def allCashLeft():
    my.left_money_buy_day1_ni_hui_gou()


def good_morning():
    my.showMyPos()


my = MyPos(xt_trader, acc)
registChecker()
if test_mode:
    # 测试任务
    good_morning()
    daily_task()
    allCashLeft()
else:
    # 早上好
    schedule.every().day.at("08:35").do(good_morning)
    # 正常买入
    schedule.every().day.at("13:19").do(daily_task)
    # 剩余资金处置
    schedule.every().day.at("10:08").do(allCashLeft)

    while True:
        schedule.run_pending()
        time.sleep(1)

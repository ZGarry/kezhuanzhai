# coding:utf-8
import time
import schedule
from MyPos import MyPos
from Settings import test_mode
from init import xt_trader, acc, init_flag
from datechecker.checkDebt import check_debt
from datechecker.DateChecker import registChecker
from dingding.XiaoHei import xiaohei
from util import today_is_trade_day
from utils.power import init_power_settings
from utils.log import setup_logging
from jisilu.jisilu_data import Jisilu
import logging

logger = logging.getLogger(__name__)

def daily_task():
    if not today_is_trade_day():
        xiaohei.send_text(f"今天非交易日，不进行交易")
        return

    # 股票信息展示
    if init_flag:
        my.showMyPos()

    # 跑策略
    if init_flag:
        my.two_low()

    # 买逆回购，剩下的资金买逆回购
    if init_flag:
        my.buy_ni_hui_gou()

def good_morning():
    # 个人股票展示
    if init_flag:
        my.showMyPos()

    # 负债提醒
    check_debt()

    # 今天是否是交易日
    is_trade_day = today_is_trade_day()
    xiaohei.send_text(f"今天是否是交易日：{is_trade_day}")

def health_reminders():
    """健康提醒"""
    xiaohei.send_text("喝水提醒: 请记得多喝水!")
    xiaohei.send_text(f"休息提醒: 每隔一小时请站起来活动一下!")

def collect_turnover():
    """收集当日换手率数据"""
    if not today_is_trade_day():
        logger.info("今日非交易日，跳过换手率数据采集")
        return
        
    jsl = Jisilu()
    df = jsl.run()
       

# 初始化日志
setup_logging()

# 初始化电源设置
init_power_settings()

# 初始化交易对象
my = MyPos(xt_trader, acc, init_flag)
registChecker()

if test_mode:
    good_morning()
    daily_task()
    collect_turnover()  # 测试模式下直接执行
else:
    schedule.every().day.at("08:35").do(good_morning)
    schedule.every().day.at("13:17").do(daily_task)
    schedule.every().day.at("16:00").do(collect_turnover)  # 每天16:00采集换手率数据
    schedule.every().hour.do(health_reminders)

    while True:
        schedule.run_pending()
        time.sleep(1)

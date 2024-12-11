# coding:utf-8
import time
import schedule
from loguru import logger
from MyPos import MyPos
from Settings import test_mode
from init import xt_trader, acc, init_flag
from datechecker.checkDebt import check_debt
from datechecker.DateChecker import registChecker
from dingding.XiaoHei import xiaohei
from data_util import today_is_trade_day
from util.power import init_power_settings, turn_off_monitor
from util.log_util import setup_logging
from jisilu.jisilu_data import Jisilu

def daily_task():
    try:
        if not today_is_trade_day():
            xiaohei.send_text(f"今天非交易日，不进行交易")
            return

        # 股票信息展示
        if init_flag:
            my.showMyPos()

        # 跑策略
        if init_flag:
            my.two_low()
            # my.composite()

        # 交易完成后关闭显示器
        logger.info("交易完成，准备关闭显示器...")
        turn_off_monitor()
        
    except Exception as e:
        logger.exception("执行每日任务失败")

def buy_reverse_repo():
    """执行逆回购交易"""
    if not today_is_trade_day():
        return
        
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
    # xiaohei.send_text(f"今天是否是交易日：{is_trade_day}")

def health_reminders():
    """健康提醒"""
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

logger.info("开始初始化电源设置...")
# 初始化电源设置
init_power_settings()
logger.info("电源设置初始化完成")

# 初始化交易对象
my = MyPos(xt_trader, acc, init_flag)
registChecker()

if test_mode:
    good_morning()
    daily_task()
    buy_reverse_repo()
    collect_turnover()  # 测试模式下直接执行
else:
    schedule.every().day.at("08:35").do(good_morning)
    schedule.every().day.at("14:44").do(daily_task)
    schedule.every().day.at("14:50").do(buy_reverse_repo)  # 新增：每天14:50执行逆回购
    schedule.every().day.at("16:00").do(collect_turnover)
    schedule.every().hour.do(health_reminders)

    while True:
        schedule.run_pending()
        time.sleep(1)

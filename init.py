import datetime
import random
import time
import schedule
from qmt.datechecker.DateChecker import registChecker
from qmt.datechecker.checkDebt import check_debt
from qmt.dingding.XiaoHei import xiaohei
from tool.weather_reminder import get_all_weather
import ctypes

import subprocess

# win系统可执行


def set_sleep_timeout(minutes):
    # 分钟转换为
    seconds = minutes
    # 使用subprocess调用powercfg命令设置显示器熄屏时间
    subprocess.call(f"powercfg /change monitor-timeout-ac {seconds}", shell=True)
    subprocess.call(f"powercfg /change monitor-timeout-dc {seconds}", shell=True)


# 这个代码是可以不提供的执行的，一天可以之心那个到底
# 设置显示器在5分钟不操作后熄屏
set_sleep_timeout(5)
# 设置系统执行状态，防止系统休眠，但允许显示器关闭
ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)

# 早上好
# 后续考虑这些上服务器


def good_morning():
    # 负债提醒
    check_debt()
    # 日常事务检查，利用schedule部分进行检查
    registChecker()
    # 天气提醒
    weather_reports = get_all_weather()
    xiaohei.send_text(weather_reports)

# 健康提醒


def health_reminders():
    print(1)
    xiaohei.send_text("喝水提醒: 请记得多喝水!")
    xiaohei.send_text(f"休息提醒: {random.random()}每隔一小时请站起来活动一下!")


# 早上好
good_morning()
schedule.every().day.at("08:00").do(good_morning)
# 每小时提醒，仅作为一个demo
schedule.every().hour.do(health_reminders)

while True:
    schedule.run_pending()
    time.sleep(1)

"""
设置，用于初始化项目and more

设置（初始多少金额，原始数据来源）
-
容器（包含所有策略，以及每个策略最后曲线）
"""

from Data import df, day2df, dateRange


class Setting:
    def __init__(self):
        # 初始资金
        self.initCash = 10000
        self.df = df  # 数据
        self.day2df = day2df  # 日数据
        self.dateRange = dateRange  # 日期范围
        pass

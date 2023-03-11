from typing import List
from Backtesting import Backtesting
from Painter import Painter
from Setting import Setting
from Data import dataFrame, day2df


class StrageyPool:
    def __init__(self, backtesterList: List[Backtesting], setting: Setting):
        self.backtesterList = backtesterList  # 回测集合
        self.setting = setting  # 设置

    def show(self):
        return [(backtester.mode, backtester.name) for backtester in self.backtesterList]

    def rebuild(self, modeNameList):
        self.backtesterList = []
        for mode, name in modeNameList:
            backtester = Backtesting(
                self.df, mode=mode, name=name, setting=self.setting)
            backtester
            self.backtesterList.append(backtester)

        # paint
        Painter(self.backtesterList).paint()

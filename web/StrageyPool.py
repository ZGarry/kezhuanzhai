from Backtesting import Backtesting
from Painter import Painter
from Setting import Setting


class StrageyPool:
    def __init__(self, setting: Setting):
        self.backtesterList = []  # 回测集合
        self.setting = setting  # 设置

    def show(self):
        return [(backtester.mode, backtester.name) for backtester in self.backtesterList]

    def add(self, mode, name):
        modeNameList = self.show()
        if (mode, name) in modeNameList:
            return False

        modeNameList.append((mode, name))
        self.rebuild(modeNameList)

    def rebuild(self, modeNameList):
        self.backtesterList = []
        for mode, name in modeNameList:
            backtester = Backtesting(
                mode=mode, name=name, setting=self.setting)
            backtester.run()
            self.backtesterList.append(backtester)

        # paint
        Painter(self.backtesterList).paint()


if __name__ == '__main__':
    strageyPool = StrageyPool(setting=Setting())
    strageyPool.rebuild([("双低","双低"),
            ("低价","低价"),
            ("100-130策略","100-130策略"),
            ("双低-下跌10%卖出","双低-下跌10%卖出"),
            ("低价-下跌10%卖出","低价-下跌10%卖出"),
            ("低价-下跌10%卖出-130卖出","低价-下跌10%卖出-130卖出")])
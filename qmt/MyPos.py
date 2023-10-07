# coding:utf-8

from xtquant import xtdata, xtconstant
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount
import pandas as pd

from qmt.Settings import test_mode
from qmt.XiaoHei import xiaohei
from qmt.util import getNameFromCode


class MyPos:
    myPos = {}
    # 全部资金，包括现金 + 当前持有资金
    allCash = None

    def __init__(self, xt_trader: XtQuantTrader, acc: StockAccount):
        self.xt_trader = xt_trader
        self.acc = acc

    def refresh(self):
        positions = self.xt_trader.query_stock_positions(self.acc)
        for pos in positions:
            self.myPos[pos.stock_code] = pos.volume

        asset = self.xt_trader.query_stock_asset(self.acc)
        self.allCash = asset.cash + asset.market_value

    def showMyPos(self):
        positions = self.xt_trader.query_stock_positions(self.acc)
        _sum = 0
        for pos in positions:
            self.myPos[pos.stock_code] = pos.volume
            print(f"股票{pos.stock_code}持有{pos.volume}股，市值{pos.market_value}，平均建仓成本{pos.open_price}")
            xiaohei.send_text(f"股票{pos.stock_code}持有{pos.volume}股")
            _sum += pos.market_value

        print(f"总市值{_sum}")

        asset = self.xt_trader.query_stock_asset(self.acc)
        self.allCash = asset.cash + asset.market_value
        print(f"现金:{asset.cash},股票持仓:{asset.market_value}")

        xiaohei.send_text(f"现金:{asset.cash}, 股票持仓:{asset.market_value}")

    def now_cb_df(self):
        ## 获取转债数据
        data = xtdata.get_full_tick(['SH', 'SZ'])
        # 获取可转债相关数据(每一行都是不一样的数据)
        df = pd.DataFrame(data).transpose()
        # https://zhuanlan.zhihu.com/p/137975171
        df = df[df.index.str.match('(110|113).*SH|(127|128|123).*SZ')]
        df = df[df['volume'] > 0]
        return df

    def buy(self, stock_code, count):
        self.xt_trader.order_stock_async(
            self.acc, stock_code, xtconstant.STOCK_BUY, count, xtconstant.LATEST_PRICE, -1, 'strategy_name',
            stock_code)
        xiaohei.send_text(f"买入{getNameFromCode(stock_code)} {count}股")

    def sell(self, stock_code, count):
        if count < 0:
            count = -count;
        self.xt_trader.order_stock_async(
            self.acc, stock_code, xtconstant.STOCK_SELL, count, xtconstant.LATEST_PRICE, -1, 'strategy_name',
            stock_code)
        xiaohei.send_text(f"卖出{getNameFromCode(stock_code)} {count}股")

    """
    获取目标预期买入股票信息
    """

    def get_want_pos(self):
        df = self.now_cb_df()

        ## 获取当前资金（从较低的开始，逐步买入，直到全部资金用完为之）
        # 预留3k做资金周转
        nowCash = self.allCash - 3000

        ## 获取目标盘数据
        wantPos = {}
        while True:
            for stock_code, stock_info in df.sort_values('lastPrice')[:10].iterrows():
                if nowCash < stock_info['lastPrice'] * 10:
                    return wantPos

                if stock_code not in wantPos:
                    wantPos[stock_code] = 10
                else:
                    wantPos[stock_code] += 10
                nowCash -= stock_info['lastPrice'] * 10

    def f_Low(self):

        ## 低价策略
        # dict1 = {"苹果": 1, "橘子": 2, "香蕉": 3}
        # dict2 = {"苹果": 2, "橘子": 2, "葡萄": 4}

        wantPos = self.get_want_pos()

        # 对两个字典做差
        diff_dict = {key: wantPos.get(key, 0) - self.myPos.get(key, 0) for key in set(self.myPos) | set(wantPos)}

        # 从小到大排序
        diff_dict = dict(sorted(diff_dict.items(), key=lambda item: item[1]))

        for key in diff_dict.keys():
            print(f"{key}应该操作{diff_dict[key]}股")

            if test_mode:
                # 测试任务
                continue

            if diff_dict[key] > 0:
                self.buy(key, diff_dict[key])
            elif diff_dict[key] < 0:
                self.sell(key, diff_dict[key])

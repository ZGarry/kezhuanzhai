# coding:utf-8
from xtquant import xtdata, xtconstant
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount
import pandas as pd

from Settings import test_mode
from qmt.dingding.XiaoHei import xiaohei
from util import getNameFromCode, s, get_all_data, to_long_name


class MyPos:
    # 里面存着当前持有股票情况
    myPos = {}
    # 全部资金，包括现金 + 当前持有资金
    allCash = None

    def __init__(self, xt_trader: XtQuantTrader, acc: StockAccount, init_flag: bool):
        self.xt_trader = xt_trader
        self.acc = acc
        self.init_flag = init_flag

    def refresh(self):
        positions = self.xt_trader.query_stock_positions(self.acc)
        for pos in positions:
            self.myPos[pos.stock_code] = pos.volume

        asset = self.xt_trader.query_stock_asset(self.acc)
        self.allCash = asset.cash + asset.market_value

    def showMyPos(self):
        positions = self.xt_trader.query_stock_positions(self.acc)
        _sum = 0
        prefix = ""
        for i, pos in enumerate(positions):
            if pos.volume <= 0:
                continue
            self.myPos[pos.stock_code] = pos.volume
            print(f"股票{pos.stock_code}持有{pos.volume}股，市值{pos.market_value}，平均建仓成本{pos.open_price}")
            prefix += f"{i + 1}.{getNameFromCode(pos.stock_code)}持有{pos.volume}股\n"
            _sum += pos.market_value

        print(f"总市值{_sum}")

        asset = self.xt_trader.query_stock_asset(self.acc)
        self.allCash = asset.cash + asset.market_value
        print(f"现金:{asset.cash},股票持仓:{asset.market_value}")
        xiaoheiStr = f"总金额:{s(_sum)},现金:{s(asset.cash)},股票持仓:{s(asset.market_value)}"

        xiaohei.send_text(f"{xiaoheiStr}\n{prefix}")

    def buy(self, stock_code, count):
        if test_mode:
            # 测试任务
            return

        self.xt_trader.order_stock_async(
            self.acc, stock_code, xtconstant.STOCK_BUY, count, xtconstant.LATEST_PRICE, -1, 'my_strategy',
            stock_code)

    def sell(self, stock_code, count):
        if test_mode:
            # 测试任务
            return

        if count < 0:
            count = -count
        self.xt_trader.order_stock_async(
            self.acc, stock_code, xtconstant.STOCK_SELL, count, xtconstant.LATEST_PRICE, -1, 'my_strategy',
            stock_code)

    def two_low_want(self, df):
        ##
        needUseMoney = 100000

        # 获取目标盘数据
        wantPos = {}
        my = list(df[:10].iterrows())
        while True:
            for index, items in my:
                if needUseMoney < items['可转债价格'] * 10:
                    return wantPos

                stock_code = to_long_name(items['可转债代码'])
                if stock_code not in wantPos:
                    wantPos[stock_code] = 10
                else:
                    wantPos[stock_code] += 10
                needUseMoney -= items['可转债价格'] * 10

    # 固定按照100一手的方式
    # 如何获得正股规模
    def buy_ni_hui_gou(self):
        asset = self.xt_trader.query_stock_asset(self.acc)
        # 剩余1k元即可
        need_buy = asset.cash - 1000
        if need_buy < 1000:
            return

        # 买入深市所有逆回购
        # 最少需要1k1k一购买
        self.sell('204001.SH', int(int(need_buy / 100) / 10) * 10)

    # 双底策略，且不买市值过低的公司
    def two_low(self):
        x = get_all_data()
        x = x[x['正股总市值'] > 50 * 10 ** 8]

        if len(x) < 10:
            raise Exception("使用50亿进行过滤后，不再有足够数量符合条件的可转债")

        # 按照'双低'列进行升序排序
        sorted_df = x.sort_values(by='双低', ascending=True)
        wantPos = self.two_low_want(sorted_df)
        # 对两个字典做差
        diff_dict = {key: wantPos.get(key, 0) - self.myPos.get(key, 0) for key in set(self.myPos) | set(wantPos)}

        # 从小到大排序
        diff_dict = dict(sorted(diff_dict.items(), key=lambda item: item[1]))
        diff_dict['888880.SH'] = 0
        # etf也不进行出售
        diff_dict['510050.SH'] = 0
        xiaoheiStr = ""
        for key in diff_dict.keys():
            print(f"{key}应该操作{diff_dict[key]}股")

            if diff_dict[key] > 0:
                self.buy(key, diff_dict[key])
                xiaoheiStr += f"买入{getNameFromCode(key)} {diff_dict[key]}股\n"
            elif diff_dict[key] < 0:
                self.sell(key, diff_dict[key])
                xiaoheiStr += f"卖出{getNameFromCode(key)} {diff_dict[key]}股\n"

        xiaohei.send_text(xiaoheiStr)

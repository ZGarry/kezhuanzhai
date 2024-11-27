# coding:utf-8
from xtquant import xtdata, xtconstant
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount
import pandas as pd
from typing import Dict, Optional
from dataclasses import dataclass
import logging

from Settings import test_mode
from dingding.XiaoHei import xiaohei
from util import getNameFromCode, show, get_all_data, to_long_name

logger = logging.getLogger(__name__)

@dataclass
class Position:
    """持仓信息数据类"""
    stock_code: str
    volume: int
    market_value: float
    open_price: float

class MyPos:
    myPos = {}
    allMoney = None

    def __init__(self, xt_trader: XtQuantTrader, acc: StockAccount, init_flag: bool):
        self.xt_trader = xt_trader
        self.acc = acc
        self.init_flag = init_flag
        self.positions: Dict[str, Position] = {}
        self.total_asset: Optional[float] = None

    def refresh(self) -> None:
        """刷新持仓信息"""
        try:
            positions = self.xt_trader.query_stock_positions(self.acc)
            self.positions.clear()
            for pos in positions:
                self.positions[pos.stock_code] = Position(
                    pos.stock_code,
                    pos.volume,
                    pos.market_value,
                    pos.open_price
                )
                
            asset = self.xt_trader.query_stock_asset(self.acc)
            self.total_asset = asset.total_asset
        except Exception as e:
            logger.error(f"刷新持仓失败: {e}")
            raise

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

        # 此处股票持仓有问题，港股通部分没有展示
        asset = self.xt_trader.query_stock_asset(self.acc)
        self.allMoney = asset.total_asset
        print(f"现金:{asset.cash},股票持仓:{asset.market_value}")
        xiaoheiStr = f"总金额:{show(_sum)},现金:{show(asset.cash)},股票持仓:{show(asset.market_value)}"

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
        needUseMoney = 200000

        # 获取目标盘数据
        wantPos = {}
        my = list(df[:10].iterrows())
        while True:
            for index, items in my:
                if needUseMoney < items['可转债价格'] * 10:
                    return wantPos

                stock_code = to_long_name(index)
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
        import jisilu.jisilu_data as jisilu_data
        data = jisilu_data.Jisilu().run()
        ndata = data[(data['转债剩余占总市值比'] < 50) & (data['剩余时间'] > 0.3)].sort_values('双低',
                                                                                               ascending=True).head(10)

        for index, name in ndata[['转债剩余占总市值比', '可转债名称', '正股代码', '双低', '可转债价格']].head(10)[
            '可转债名称'].items():
            print(f"可转债代码: {index}, 可转债名称: {name}")

        if len(ndata) < 10:
            raise Exception("进行过滤后，不再有足够数量符合条件的可转债")

        # 按照'双低'列进行升序排序
        wantPos = self.two_low_want(ndata)
        # 对两个字典做差
        diff_dict = {key: wantPos.get(key, 0) - self.myPos.get(key, 0) for key in set(self.myPos) | set(wantPos)}

        # 从小到大排序
        diff_dict = dict(sorted(diff_dict.items(), key=lambda item: item[1]))
        # 设置非12、11开头的代码为0
        for key in list(diff_dict.keys()):
            if not key.startswith(('12', '11')):
                diff_dict[key] = 0
            if '110092' in key:
                diff_dict[key] = 0

        xiaoheiStr = ""
        # 解决一下买入的时候可用资金不足的问题，需要预留一些资金，然后继续挂单
        # 逆回购放到最后
        for key in diff_dict.keys():
            print(f"{key}应该操作{diff_dict[key]}股")

            if diff_dict[key] > 0:
                self.buy(key, diff_dict[key])
                xiaoheiStr += f"买入{getNameFromCode(key)} {diff_dict[key]}股\n"
            elif diff_dict[key] < 0:
                self.sell(key, diff_dict[key])
                xiaoheiStr += f"卖出{getNameFromCode(key)} {diff_dict[key]}股\n"

        xiaohei.send_text(xiaoheiStr)

class Position:
    def __init__(self):
        # 使用类型注解提高代码可读性
        self.positions: Dict[str, float] = {}
        
    def update_position(self, symbol: str, quantity: float) -> None:
        """更新持仓信息
        
        Args:
            symbol: 股票代码
            quantity: 持仓数量
        """
        self.positions[symbol] = quantity

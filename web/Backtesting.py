
from Setting import Setting
from Painter import Painter

need_log = False


def printL(s):
    if need_log:
        print(s)


class Backtesting:
    def __init__(self, mode="双低", name="default", setting=Setting()):
        self.mode = mode  # 支持的策略
        self.name = name  # 策略名称
        self.setting = setting  # 设置

        self.df = self.setting.df  # 总数据
        self.day2df = self.setting.day2df  # 日数据
        self.dateRange = self.setting.dateRange  # 时间范围

        self.myPosition = {}  # 当前持仓列表
        self.posHigh = {}  # 持仓股票的最高位
        self.myCash = setting.initCash  # 现金
        self.myHoldNum = 10  # 持债支数

        self.posValueList = []  # 市值变化列表
        self.today_low = None  # 今日低价格数据(可买入部分)
        self.today_df = None

    def dont_have_value(self, name):
        return len(self.today_df[self.today_df['secShortNameBond']
                                 == name]) == 0

    # 获取某某股票的上一份价格
    def get_last_price(self, name):
        try:
            price = self.today_df[self.today_df['secShortNameBond']
                                  == name]['closePriceBond'].iloc[0]
        except:
            # printL(f'{date_str},{name}已退市，未读取到数据')
            price = self.df[self.df['secShortNameBond']
                            == name].iloc[-1]['closePriceBond']
            return price
        return price

    # 每日运行
    def run(self):
        # 缓存机制
        import os
        cache_file = os.sep.join(
            [os.getcwd(), "build", f"{self.name}_result.txt"])
        if os.path.exists(cache_file):
            print("本地已有缓存")
            with open(cache_file) as f:
                self.posValueList = list(
                    map(lambda x: float(x), f.read().split(",")))
            return

        for today_date in self.setting.dateRange:
            printL(f'-----今日{today_date}')
            self.today_df = self.setting.day2df[today_date]
            self.preCheck()

            self.sell_all()

            self.buy_all()

            self.afterCheck()

        # save
        if not os.path.exists(cache_file):
            with open(file=cache_file, mode='w') as f:
                li = map(lambda x: str(x), self.posValueList)
                f.write(",".join(li))

    # 检查当日数据
    def preCheck(self):
        #   每日低价
        if self.mode.startswith("双低"):
            today_df_low = self.today_df.sort_values('doubleLow')[
                :self.myHoldNum]
        elif self.mode.startswith("低价"):
            today_df_low = self.today_df.sort_values('closePriceBond')[
                :self.myHoldNum]
        elif self.mode == "100-130策略":
            today_df_low = self.today_df[self.today_df['closePriceBond'] <= 100]
        self.today_low = set(today_df_low['secShortNameBond'])

        # 对应股票最高价格更新
        for pos in self.myPosition:
            self.posHigh[pos] = max(self.posHigh.get(
                pos, 0), self.get_last_price(pos))

    # 检查当日市值
    def afterCheck(self):
        # 进入新的一天，计算当前市值
        today_pos_value = sum(self.get_last_price(
            pos)*self.myPosition[pos] for pos in self.myPosition) + self.myCash
        printL(f'今日总市值{today_pos_value}')
        self.posValueList.append(today_pos_value)

    def sell_all(self):
        # 卖出
        need_sell = []
        for pos in self.myPosition.keys():
            # 如果明日退市了,今日需卖出
            if self.dont_have_value(pos):
                need_sell.append(pos)
            elif self.mode == "100-130策略" and self.get_last_price(pos) >= 130:
                need_sell.append(pos)
            elif self.mode.endswith("下跌10%卖出") and self.get_last_price(pos) <= self.posHigh[pos] * 0.9:
                need_sell.append(pos)
            elif self.mode.endswith("下跌10%卖出-130卖出") and self.get_last_price(pos) <= self.posHigh[pos] * 0.9 and self.get_last_price(pos) >= 130:
                need_sell.append(pos)
            else:
                # 低价策略
                if pos in self.today_low:
                    continue
                else:
                    need_sell.append(pos)
        for pos in need_sell:
            self.sell(pos)

    def buy_all(self):
        if self.myCash == 0:
            printL("无资金")
            return

        # 买入
        # 计算需买入
        need_buy = []
        # 低价区间的全部买入
        for pos in self.today_low:
            if pos in self.myPosition.keys():
                #         已持有
                continue
            else:
                #         未持有
                need_buy.append(pos)

        #  均匀分配资金到买入，此处姑且视为可以买入带小数点的股票
        if len(need_buy) != 0:
            can_buy_cash = self.myCash/len(need_buy)
            for item in need_buy:
                self.buy(item, can_buy_cash)
        else:
            printL("无可购买标的")

    def buy(self, name, cash):
        price = self.get_last_price(name)
        printL(f'以{price}买入{name}#{cash}钱,共{cash/price}股')
        self.myCash -= cash
        self.myPosition[name] = cash/price

    def sell(self, name):
        price = self.get_last_price(name)
        printL(f'以{price}卖出{name}#{self.myPosition[name]}股')
        self.myCash += price * self.myPosition[name]
        del self.myPosition[name]


# 获取所有回测数据


# backtester = Backtesting(mode="双低", name="双低", setting=Setting())
# backtester.run()

# backtester2 = Backtesting(dataFrame, mode="低价", name="低价")
# backtester2.run()

# backtester3 = Backtesting(dataFrame, mode="100-130策略", name="100-130策略")
# backtester3.run()

# backtester4 = Backtesting(dataFrame, mode="双低-下跌10%卖出", name="双低-下跌10%卖出")
# backtester4.run()

# backtester5 = Backtesting(dataFrame, mode="低价-下跌10%卖出", name="低价-下跌10%卖出")
# backtester5.run()

# backtester6 = Backtesting(
#     dataFrame, mode="低价-下跌10%卖出-130卖出", name="低价-下跌10%卖出-130卖出")
# backtester6.run()

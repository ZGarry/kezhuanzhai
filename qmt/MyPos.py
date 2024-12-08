from typing import Optional
from trading.position import PositionManager
from trading.executor import TradeExecutor
from strategy.two_low import TwoLowStrategy
from strategy.turnover import TurnoverStrategy
from strategy.reverse_repo import ReverseRepoStrategy
from reporter import PositionReporter
from trading.strategy_executor import StrategyExecutor

class MyPos:
    """交易管理类"""
    def __init__(self, xt_trader, acc, init_flag: bool):
        self.init_flag = init_flag
        
        # 初始化各个组件
        self.position_manager = PositionManager(xt_trader, acc)
        self.trade_executor = TradeExecutor(xt_trader, acc)
        self.reporter = PositionReporter(self.position_manager)
        self.strategy_executor = StrategyExecutor(self.position_manager, self.trade_executor)
        
        # 初始化策略
        self.two_low_strategy = TwoLowStrategy()
        self.turnover_strategy = TurnoverStrategy()
        self.reverse_repo_strategy = ReverseRepoStrategy(self.position_manager, self.trade_executor)
        
    def showMyPos(self) -> None:
        """显示当前持仓"""
        self.reporter.report()
        
    def two_low(self) -> None:
        """执行双低策略"""
        self.strategy_executor.execute_strategy(self.two_low_strategy)
        
    def turnover(self) -> None:
        """执行换手率策略"""
        self.strategy_executor.execute_strategy(self.turnover_strategy)
        
    def buy_ni_hui_gou(self) -> None:
        """执行逆回购策略"""
        self.reverse_repo_strategy.execute()

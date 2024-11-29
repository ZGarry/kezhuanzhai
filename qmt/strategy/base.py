from abc import ABC, abstractmethod
from trading.position import PositionManager
from trading.executor import TradeExecutor

class Strategy(ABC):
    """策略基类"""
    def __init__(self, position_manager: PositionManager, trade_executor: TradeExecutor):
        self.position_manager = position_manager
        self.trade_executor = trade_executor
        
    @abstractmethod
    def execute(self) -> None:
        """执行策略"""
        pass 
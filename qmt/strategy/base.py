from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    """策略基类"""
    @abstractmethod
    def filter_and_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """执行策略的筛选和评分"""
        pass 
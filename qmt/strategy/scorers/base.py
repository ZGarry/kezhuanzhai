from abc import ABC, abstractmethod
import pandas as pd

class BaseScorer(ABC):
    """评分器基类"""
    @abstractmethod
    def score(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算评分"""
        pass 
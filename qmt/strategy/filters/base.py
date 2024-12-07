from abc import ABC, abstractmethod
import pandas as pd

class BaseFilter(ABC):
    """过滤器基类"""
    @abstractmethod
    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """执行过滤逻辑"""
        pass 
from strategy.filters.base import BaseFilter
import pandas as pd

class BasicFilter(BaseFilter):
    """基础过滤条件"""
    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        基础过滤条件:
        1. 转债剩余占总市值比 < 50%
        2. 剩余时间 > 0.3年
        """
        return df[(df['转债剩余占总市值比'] < 50) & 
                 (df['剩余时间'] > 0.3)] 
from strategy.scorers.base import BaseScorer
import pandas as pd

class DoubleLowScorer(BaseScorer):
    """双低评分"""
    def score(self, df: pd.DataFrame) -> pd.DataFrame:
        """基于双低因子进行排序"""
        return df.sort_values('双低', ascending=True) 
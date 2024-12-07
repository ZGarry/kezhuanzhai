from typing import Dict
import logging
import pandas as pd
from strategy.base import Strategy
from strategy.filters.basic_filter import BasicFilter
from strategy.scorers.turnover_scorer import TurnoverScorer

logger = logging.getLogger(__name__)

class TurnoverStrategy(Strategy):
    """换手率策略"""
    def __init__(self):
        self.basic_filter = BasicFilter()
        self.turnover_scorer = TurnoverScorer()
        
    def filter_and_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        执行换手率策略的筛选和评分
        Returns:
            pd.DataFrame: 筛选和评分后的数据
        """
        # 应用过滤器
        filtered_data = self.basic_filter.filter(df)
        
        # 应用评分器并获取前10名
        return self.turnover_scorer.score(filtered_data).head(10) 
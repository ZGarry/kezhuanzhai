from typing import Dict
import logging
import pandas as pd
from strategy.base import Strategy
from strategy.filters.basic_filter import BasicFilter
from strategy.scorers.composite_scorer import CompositeScorer

logger = logging.getLogger(__name__)

class CompositeStrategy(Strategy):
    """复合策略(双低+换手率)"""
    def __init__(self):
        self.basic_filter = BasicFilter()
        self.composite_scorer = CompositeScorer()
        
    def filter_and_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        执行复合策略的筛选和评分
        Returns:
            pd.DataFrame: 筛选和评分后的数据
        """
        # 应用过滤器
        filtered_data = self.basic_filter.filter(df)
        
        # 应用评分器并获取前10名
        return self.composite_scorer.score(filtered_data).head(10) 
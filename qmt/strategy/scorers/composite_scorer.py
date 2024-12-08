from strategy.scorers.base import BaseScorer
import pandas as pd
import numpy as np

class CompositeScorer(BaseScorer):
    """复合评分器(双低+换手率)"""
    def score(self, df: pd.DataFrame) -> pd.DataFrame:
        """基于双低和五日平均换手率的复合评分
        """
                
        # 计算双低的排名得分(升序排名,值越小得分越高)
        df['双低得分'] = df['双低'].rank(ascending=True)
        
        # 计算换手率的排名得分(降序排名,值越大得分越高)
        df['换手率得分'] = df['五日平均换手率'].rank(ascending=False)
        
        # 归一化得分(转换到0-1区间)
        total_count = len(df)
        df['双低得分'] = df['双低得分'] / total_count
        df['换手率得分'] = df['换手率得分'] / total_count
        
        # 计算复合得分(可以调整权重)
        双低权重 = 0.6  # 双低因子权重60%
        换手率权重 = 0.4  # 换手率因子权重40%
        
        df['复合得分'] = (df['双低得分'] * 双低权重 + 
                      df['换手率得分'] * 换手率权重)
        
        # 按复合得分降序排序(得分越高排名越靠前)
        result = df.sort_values('复合得分', ascending=False)
    
        return result
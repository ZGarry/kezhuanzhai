from strategy.scorers.base import BaseScorer
import pandas as pd

class TurnoverScorer(BaseScorer):
    """换手率评分器"""
    def score(self, df: pd.DataFrame) -> pd.DataFrame:
        """基于五日平均换手率进行排序
        
        Args:
            df: 包含五日平均换手率数据的DataFrame
            
        Returns:
            按五日平均换手率降序排序的DataFrame
        """
        # 确保五日平均换手率列存在
        if '五日平均换手率' not in df.columns:
            raise ValueError("数据中缺少'五日平均换手率'列")
            
        # 按五日平均换手率降序排序(换手率越高分数越高)
        return df.sort_values('五日平均换手率', ascending=False)

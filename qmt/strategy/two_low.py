from typing import Dict
import logging
from strategy.base import Strategy
from data_util import to_long_name
from dingding.XiaoHei import xiaohei
from strategy.filters.basic_filter import BasicFilter
from strategy.scorers.double_low_scorer import DoubleLowScorer

logger = logging.getLogger(__name__)

class TwoLowStrategy(Strategy):
    """双低策略"""
    def __init__(self, position_manager, trade_executor):
        super().__init__(position_manager, trade_executor)
        self.basic_filter = BasicFilter()
        self.double_low_scorer = DoubleLowScorer()
        
    def two_low_want(self, df) -> Dict[str, int]:
        needUseMoney = 300000
        wantPos = {}
        my = list(df[:10].iterrows())
        
        while True:
            for index, items in my:
                if needUseMoney < items['可转债价格'] * 10:
                    return wantPos

                stock_code = to_long_name(index)
                if stock_code not in wantPos:
                    wantPos[stock_code] = 10
                else:
                    wantPos[stock_code] += 10
                needUseMoney -= items['可转债价格'] * 10
                
    def execute(self) -> None:
        """执行双低策略"""
        import jisilu.jisilu_data as jisilu_data
        
        # 获取数据
        data = jisilu_data.Jisilu().run()
        
        # 应用过滤器
        filtered_data = self.basic_filter.filter(data)
        
        # 应用评分器并获取前10名
        scored_data = self.double_low_scorer.score(filtered_data).head(10)
                    
        # 计算目标持仓
        wantPos = self.two_low_want(scored_data)
        current_pos = {k: v.volume for k, v in self.position_manager.get_all_positions().items()}
        
        # 计算差异
        diff_dict = {key: wantPos.get(key, 0) - current_pos.get(key, 0) 
                    for key in set(current_pos) | set(wantPos)}
                    
        # 过滤和排序
        diff_dict = dict(sorted(diff_dict.items(), key=lambda item: item[1]))
        
        # 执行交易
        xiaoheiStr = self._execute_trades(diff_dict)
        
        if xiaoheiStr:
            xiaohei.send_text(xiaoheiStr)
            
    def _execute_trades(self, diff_dict: Dict[str, int]) -> str:
        """执行交易并返回消息文本"""
        from data_util import getNameFromCode
        xiaoheiStr = ""
        
        for key in list(diff_dict.keys()):
            if not key.startswith(('12', '11')) or '110092' or '123099' in key:
                diff_dict[key] = 0
                
        for key, diff in diff_dict.items():
            if diff > 0:
                self.trade_executor.buy(key, diff)
                xiaoheiStr += f"买入{getNameFromCode(key)} {diff}股\n"
            elif diff < 0:
                self.trade_executor.sell(key, -diff)
                xiaoheiStr += f"卖出{getNameFromCode(key)} {-diff}股\n"
                
        return xiaoheiStr
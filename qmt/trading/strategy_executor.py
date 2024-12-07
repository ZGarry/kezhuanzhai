from typing import Dict, Protocol
import pandas as pd
from data_util import to_long_name, getNameFromCode
from dingding.XiaoHei import xiaohei
import logging

logger = logging.getLogger(__name__)

class Strategy(Protocol):
    def filter_and_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """策略接口"""
        pass

class StrategyExecutor:
    """策略执行器"""
    def __init__(self, position_manager, trade_executor):
        self.position_manager = position_manager
        self.trade_executor = trade_executor
        
    def calculate_target_positions(self, df: pd.DataFrame) -> Dict[str, int]:
        """计算目标持仓"""
        needUseMoney = 300000
        wantPos = {}
        my = list(df.iterrows())
        
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

    def execute_strategy(self, strategy: Strategy) -> None:
        """执行策略"""
        import jisilu.jisilu_data as jisilu_data
        
        # 获取数据
        data = jisilu_data.Jisilu().run()
        if data is None:
            logger.error("获取集思录数据失败")
            return
            
        # 应用策略的筛选和评分
        scored_data = strategy.filter_and_score(data)
        
        # 计算目标持仓
        target_positions = self.calculate_target_positions(scored_data)
        current_positions = {k: v.volume for k, v in self.position_manager.get_all_positions().items()}
        
        # 计算差异
        diff_dict = {key: target_positions.get(key, 0) - current_positions.get(key, 0) 
                    for key in set(current_positions) | set(target_positions)}
                    
        # 过滤和排序
        diff_dict = dict(sorted(diff_dict.items(), key=lambda item: item[1]))
        
        # 执行交易
        trade_msg = self._execute_trades(diff_dict)
        
        if trade_msg:
            xiaohei.send_text(trade_msg)
            
    def _execute_trades(self, diff_dict: Dict[str, int]) -> str:
        """执行交易并返回消息文本"""
        trade_msg = ""
        
        # 过滤非可转债代码
        for key in list(diff_dict.keys()):
            if not key.startswith(('12', '11')) or '110092' or '123099' in key:
                diff_dict[key] = 0
                
        # 执行交易
        for key, diff in diff_dict.items():
            if diff > 0:
                self.trade_executor.buy(key, diff)
                trade_msg += f"买入{getNameFromCode(key)} {diff}股\n"
            elif diff < 0:
                self.trade_executor.sell(key, -diff)
                trade_msg += f"卖出{getNameFromCode(key)} {-diff}股\n"
                
        return trade_msg 
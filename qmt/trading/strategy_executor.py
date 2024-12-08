from typing import Dict, Protocol
import pandas as pd
from data_util import to_long_name, getNameFromCode
from dingding.XiaoHei import xiaohei
import logging
import os

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
            
        # 合并换手率数据
        data = self.merge_turnover_data(data)
        
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
            if not key.startswith(('12', '11')) or '110092' in key:
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
    
    def merge_turnover_data(self, current_data: pd.DataFrame) -> pd.DataFrame:
        """合并当日和历史换手率数据"""
        try:
            # 读取历史换手率数据
            turnover_file = r"D:\my\kezhuanzhai\qmt\data\turnover_rates.csv"
            if not os.path.exists(turnover_file):
                logger.warning("找不到历史换手率数据文件")
                return current_data
            
            # 读取历史数据
            hist_data = pd.read_csv(turnover_file)
            
            from data_util import get_last_n_trade_days, today_is_trade_day
            
            # 根据是否为交易日获取不同天数的历史数据
            if today_is_trade_day():
                recent_dates = get_last_n_trade_days(5)  # 获取过去4个交易日
                recent_dates = recent_dates[:-1]
            else:
                recent_dates = get_last_n_trade_days(5)  # 获取过去5个交易日
                
            recent_dates = [d.strftime('%Y-%m-%d') for d in recent_dates]
            
            # 检查每个日期是否都存在于历史数据中
            for date in recent_dates:
                if date not in hist_data['date'].values:
                    raise ValueError(f"历史数据中缺少日期 {date} 的数据")
            
            # 筛选历史数据
            hist_data = hist_data[hist_data['date'].isin(recent_dates)]
            
            # 数据透视表得到每个转债的历史换手率
            pivot_data = hist_data.pivot(index='可转债代码', columns='date', values='换手率')

            # 合并回原始数据（新增了一个五日平均换手率数据）
            # 确保索引类型一致
            pivot_data.index = pivot_data.index.astype(str)
            current_data.index = current_data.index.astype(str)

            # 如果是交易日，添加当日数据
            if today_is_trade_day():
                current_turnover = current_data['换手率'].copy()
                pivot_data['current'] = current_turnover
            
            # 计算5日平均换手率
            pivot_data['五日平均换手率'] = pivot_data.mean(axis=1)

            # 使用map方法合并数据
            current_data['五日平均换手率'] = current_data.index.map(pivot_data['五日平均换手率'])
            
            return current_data
            
        except Exception as e:
            logger.error(f"合并换手率数据失败: {e}")
            return current_data

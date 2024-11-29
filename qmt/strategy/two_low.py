from typing import Dict
import logging
from strategy.base import Strategy
from util import to_long_name, getNameFromCode
from dingding.XiaoHei import xiaohei
import pandas as pd

logger = logging.getLogger(__name__)

class TwoLowStrategy(Strategy):
    """双低策略"""
    def two_low_want(self, df) -> Dict[str, int]:
        needUseMoney = 200000
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
                
    def get_turnover_history(self, bond_code: str, days: int = 5) -> float:
        """获取历史换手率数据"""
        try:
            df = pd.read_csv("data/turnover_rates.csv")
            df['date'] = pd.to_datetime(df['date'])
            recent_data = df[df.index == bond_code].tail(days)
            return recent_data['换手率'].mean() if not recent_data.empty else 0.0
        except Exception as e:
            logger.error(f"获取换手率数据失败: {e}")
            return 0.0
        
    def execute(self) -> None:
        """执行双低策略"""
        import jisilu.jisilu_data as jisilu_data
        data = jisilu_data.Jisilu().run()
        ndata = data[(data['转债剩余占总市值比'] < 50) & (data['剩余时间'] > 0.3)].sort_values(
            '双低', ascending=True).head(10)
            
        if len(ndata) < 10:
            raise Exception("进行过滤后，不再有足够数量符合条件的可转债")
            
        # 计算目标持仓
        wantPos = self.two_low_want(ndata)
        current_pos = {k: v.volume for k, v in self.position_manager.get_all_positions().items()}
        
        # 计算差异
        diff_dict = {key: wantPos.get(key, 0) - current_pos.get(key, 0) 
                    for key in set(current_pos) | set(wantPos)}
                    
        # 过滤和排序
        diff_dict = dict(sorted(diff_dict.items(), key=lambda item: item[1]))
        for key in list(diff_dict.keys()):
            if not key.startswith(('12', '11')) or '110092' in key:
                diff_dict[key] = 0
                
        # 执行交易
        xiaoheiStr = ""
        for key, diff in diff_dict.items():
            if diff > 0:
                self.trade_executor.buy(key, diff)
                xiaoheiStr += f"买入{getNameFromCode(key)} {diff}股\n"
            elif diff < 0:
                self.trade_executor.sell(key, -diff)
                xiaoheiStr += f"卖出{getNameFromCode(key)} {-diff}股\n"
                
        if xiaoheiStr:
            xiaohei.send_text(xiaoheiStr) 
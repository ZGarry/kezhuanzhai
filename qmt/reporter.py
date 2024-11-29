from typing import Dict
import logging
from trading.position import PositionManager
from util import getNameFromCode, show
from dingding.XiaoHei import xiaohei

logger = logging.getLogger(__name__)

class PositionReporter:
    """持仓报告器"""
    def __init__(self, position_manager: PositionManager):
        self.position_manager = position_manager
        
    def report(self) -> None:
        """生成并发送持仓报告"""
        try:
            self.position_manager.refresh()
            positions = self.position_manager.get_all_positions()
            
            _sum = sum(pos.market_value for pos in positions.values())
            prefix = ""
            
            # 按代码排序（转债放后面）
            sorted_positions = sorted(
                positions.items(), 
                key=lambda x: (x[0].startswith('12'), x[0].startswith('11'))
            )
            
            for i, (code, pos) in enumerate(sorted_positions):
                if pos.volume <= 0:
                    continue
                prefix += f"{i + 1}.{getNameFromCode(code)}持有{pos.volume}股\n"
                
            asset = self.position_manager.xt_trader.query_stock_asset(self.position_manager.acc)
            msg = (f"总金额:{show(_sum)},现金:{show(asset.cash)},"
                  f"股票持仓:{show(asset.market_value)}\n{prefix}")
            
            xiaohei.send_text(msg)
            
        except Exception as e:
            logger.error(f"生成持仓报告失败: {e}")
            raise 
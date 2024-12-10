from typing import Dict
import logging
from trading.position import PositionManager
from data_util import getNameFromCode, show
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
            
            # 分离股票和转债
            stock_positions = []
            bond_positions = []
            
            for code, pos in positions.items():
                if pos.volume <= 0:
                    continue
                if code.startswith(('11', '12')):
                    bond_positions.append((code, pos))
                else:
                    stock_positions.append((code, pos))
            
            # 生成报告文本
            msg = []
            asset = self.position_manager.xt_trader.query_stock_asset(self.position_manager.acc)
            
            # 资产概览
            msg.append("==== 资产概览(不含港股) ====")
            msg.append(f"总金额: {show(asset.cash + asset.market_value)}")
            msg.append(f"现金: {show(asset.cash)}")
            msg.append(f"持仓市值: {show(asset.market_value)}")
            
            # 股票持仓
            if stock_positions:
                msg.append("==== 股票持仓 ====")
                for i, (code, pos) in enumerate(stock_positions, 1):
                    msg.append(f"{i}. {getNameFromCode(code):<8} {pos.volume:>6}股")
            
            # 转债持仓
            if bond_positions:
                msg.append("==== 转债持仓 ====")
                for i, (code, pos) in enumerate(bond_positions, 1):
                    msg.append(f"{i}. {getNameFromCode(code):<8} {pos.volume:>6}股")
            
            # 发送消息
            xiaohei.send_text("\n".join(msg))
            
        except Exception as e:
            logger.error(f"生成持仓报告失败: {e}")
            raise
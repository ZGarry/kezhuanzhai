from dataclasses import dataclass
from typing import Dict, Optional
import logging
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount

logger = logging.getLogger(__name__)

@dataclass
class Position:
    """持仓信息数据类
    
    Attributes:
        account_type: 账号类型
        account_id: 资金账号
        stock_code: 证券代码
        volume: 持仓数量
        can_use_volume: 可用数量
        open_price: 开仓价
        market_value: 市值
        frozen_volume: 冻结数量
        on_road_volume: 在途股份
        yesterday_volume: 昨日持仓
        avg_price: 成本价
        direction: 多空方向(股票不适用)
    """
    stock_code: str
    volume: int  # 持仓数量
    can_use_volume: int  # 可用数量
    open_price: float  # 开仓价
    market_value: float  # 市值
    frozen_volume: int  # 冻结数量
    on_road_volume: int  # 在途股份
    yesterday_volume: int  # 昨日持仓
    avg_price: float  # 成本价
    account_type: int  # 账号类型
    account_id: str  # 资金账号
    direction: Optional[int] = None  # 多空方向,股票不适用

class PositionManager:
    """持仓管理类"""
    def __init__(self, xt_trader: XtQuantTrader, acc: StockAccount):
        self.xt_trader = xt_trader
        self.acc = acc
        self.positions: Dict[str, Position] = {}
        self.total_asset: Optional[float] = None
        
    def refresh(self) -> None:
        """刷新持仓信息"""
        try:
            positions = self.xt_trader.query_stock_positions(self.acc)
            self.positions.clear()
            for pos in positions:
                self.positions[pos.stock_code] = Position(
                    stock_code=pos.stock_code,
                    volume=pos.volume,
                    can_use_volume=pos.can_use_volume,
                    open_price=pos.open_price,
                    market_value=pos.market_value,
                    frozen_volume=pos.frozen_volume,
                    on_road_volume=pos.on_road_volume,
                    yesterday_volume=pos.yesterday_volume,
                    avg_price=pos.avg_price,
                    account_type=pos.account_type,
                    account_id=pos.account_id,
                    direction=pos.direction if hasattr(pos, 'direction') else None
                )
                
            asset = self.xt_trader.query_stock_asset(self.acc)
            self.total_asset = asset.total_asset
        except Exception as e:
            logger.error(f"刷新持仓失败: {e}")
            raise
            
    def get_position(self, stock_code: str) -> Optional[Position]:
        """获取指定股票持仓
        
        Args:
            stock_code: 股票代码
            
        Returns:
            Position: 持仓信息对象,如果不存在则返回None
        """
        return self.positions.get(stock_code)
        
    def get_all_positions(self) -> Dict[str, Position]:
        """获取所有持仓
        
        Returns:
            Dict[str, Position]: 股票代码到持仓信息的映射
        """
        return self.positions
        
    def get_total_asset(self) -> Optional[float]:
        """获取总资产
        
        Returns:
            float: 总资产,如果未刷新则返回None
        """
        return self.total_asset
from typing import Optional
import logging
from xtquant import xtconstant
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount
from Settings import test_mode
from data_util import getNameFromCode

logger = logging.getLogger(__name__)

class TradeExecutor:
    """交易执行器"""
    def __init__(self, xt_trader: XtQuantTrader, acc: StockAccount):
        self.xt_trader = xt_trader
        self.acc = acc
        self.trade_logger = logging.getLogger('trade')
        
    def log_trade(self, action: str, stock_code: str, count: int, 
                  price: float = None, status: str = "已提交") -> None:
        """记录交易日志"""
        try:
            stock_name = getNameFromCode(stock_code)
            price_str = f"价格:{price}" if price else "市价"
            message = (f"{action} - 代码:{stock_code}({stock_name}) - "
                      f"数量:{count} - {price_str} - 状态:{status}")
            self.trade_logger.info(message)
        except Exception as e:
            logger.error(f"记录交易日志失败: {e}")
            
    def buy(self, stock_code: str, count: int) -> None:
        """买入股票"""
        if test_mode:
            self.log_trade("买入", stock_code, count, status="测试模式")
            return

        try:
            self.xt_trader.order_stock_async(
                self.acc, stock_code, xtconstant.STOCK_BUY, count, 
                xtconstant.LATEST_PRICE, -1, 'my_strategy', stock_code
            )
            self.log_trade("买入", stock_code, count)
        except Exception as e:
            self.log_trade("买入", stock_code, count, status=f"失败-{str(e)}")
            logger.error(f"买入失败: {e}")
            raise
            
    def sell(self, stock_code: str, count: int) -> None:
        """卖出股票"""
        if test_mode:
            self.log_trade("卖出", stock_code, count, status="测试模式")
            return

        try:
            if count < 0:
                count = -count
            self.xt_trader.order_stock_async(
                self.acc, stock_code, xtconstant.STOCK_SELL, count,
                xtconstant.LATEST_PRICE, -1, 'my_strategy', stock_code
            )
            self.log_trade("卖出", stock_code, count)
        except Exception as e:
            self.log_trade("卖出", stock_code, count, status=f"失败-{str(e)}")
            logger.error(f"卖出失败: {e}")
            raise 
import logging
from Settings import test_mode
from data_util import show
from dingding.XiaoHei import xiaohei

logger = logging.getLogger(__name__)

class ReverseRepoStrategy:
    """逆回购策略"""
    def __init__(self, position_manager, trade_executor):
        self.position_manager = position_manager
        self.trade_executor = trade_executor
        
    def execute(self) -> None:
        """执行逆回购策略"""
        try:
            asset = self.position_manager.xt_trader.query_stock_asset(self.position_manager.acc)
            need_buy = asset.cash - 1000
            
            if need_buy < 1000:
                return
                
            # 买入深市所有逆回购
            amount = int(int(need_buy / 100) / 10) * 10
            self.trade_executor.sell('204001.SH', amount)
            
            # 发送通知
            msg = []
            if test_mode:
                msg.append("【测试模式】")
            msg.append("==== 逆回购委托 ====")
            msg.append(f"GC001    {amount:>5}股")
            msg.append(f"剩余现金: {show(asset.cash - amount * 100)}")
            
            xiaohei.send_text("\n".join(msg))
            
        except Exception as e:
            logger.error(f"执行逆回购策略失败: {e}")
            raise
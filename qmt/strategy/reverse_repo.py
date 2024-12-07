class ReverseRepoStrategy:
    """逆回购策略"""
    def __init__(self, position_manager, trade_executor):
        self.position_manager = position_manager
        self.trade_executor = trade_executor
        
    def execute(self) -> None:
        """执行逆回购策略"""
        asset = self.position_manager.xt_trader.query_stock_asset(self.position_manager.acc)
        need_buy = asset.cash - 1000
        
        if need_buy < 1000:
            return
            
        # 买入深市所有逆回购
        self.trade_executor.sell('204001.SH', int(int(need_buy / 100) / 10) * 10)
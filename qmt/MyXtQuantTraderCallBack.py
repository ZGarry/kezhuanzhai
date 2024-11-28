import datetime
import sys
from xtquant.xttrader import XtQuantTraderCallback
import logging


class MyXtQuantTraderCallback(XtQuantTraderCallback):
    def __init__(self):
        super().__init__()
        self.trade_logger = logging.getLogger('trade')

    def on_disconnected(self):
        """
        连接断开
        :return:
        """
        print(datetime.datetime.now(), '连接断开回调')

    def on_stock_order(self, order):
        """
        委托回报推送
        :param order: XtOrder对象
        :return:
        """
        message = (f"委托回调 - 代码:{order.stock_code} - "
                  f"状态:{order.status} - 委托价格:{order.price} - "
                  f"委托数量:{order.volume} - 备注:{order.order_remark}")
        self.trade_logger.info(message)

    def on_stock_trade(self, trade):
        """
        成交变动推送
        :param trade: XtTrade对象
        :return:
        """
        message = (f"成交回调 - 代码:{trade.stock_code} - "
                  f"成交价格:{trade.price} - 成交数量:{trade.volume} - "
                  f"备注:{trade.order_remark}")
        self.trade_logger.info(message)

    def on_order_error(self, order_error):
        """
        委托失败推送
        :param order_error:XtOrderError 对象
        :return:
        """
        message = (f"委托错误 - 备注:{order_error.order_remark} - "
                  f"错误信息:{order_error.error_msg}")
        self.trade_logger.error(message)

    def on_cancel_error(self, cancel_error):
        """
        撤单失败推送
        :param cancel_error: XtCancelError 对象
        :return:
        """
        print(datetime.datetime.now(), sys._getframe().f_code.co_name)

    def on_order_stock_async_response(self, response):
        """
        异步下单回报推送
        :param response: XtOrderResponse 对象
        :return:
        """
        print(f"异步委托回调 {response.order_remark}")

    def on_cancel_order_stock_async_response(self, response):
        """
        :param response: XtCancelOrderResponse 对象
        :return:
        """
        print(datetime.datetime.now(), sys._getframe().f_code.co_name)

    def on_account_status(self, status):
        """
        :param response: XtAccountStatus 对象
        :return:
        """
        print(datetime.datetime.now(), sys._getframe().f_code.co_name)

    def on_stock_asset(self, asset):
        """
        资金变动推送
        :param asset: XtAsset对象
        :return:
        """
        print("on asset callback")
        print(asset.account_id, asset.cash, asset.total_asset)

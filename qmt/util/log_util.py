import os
import logging
import logging.handlers

def setup_logging():
    """配置日志设置"""
    # 创建logs目录
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    # 配置根日志记录器
    logging.basicConfig(level=logging.INFO,
                       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # 创建交易日志记录器
    trade_logger = logging.getLogger('trade')
    trade_logger.setLevel(logging.INFO)
    
    # 创建按天轮转的文件处理器
    trade_handler = logging.handlers.TimedRotatingFileHandler(
        'logs/trade.log',
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    trade_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    trade_logger.addHandler(trade_handler) 
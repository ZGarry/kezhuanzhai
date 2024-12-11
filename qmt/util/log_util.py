from loguru import logger
import sys
import os

def setup_logging():
    """配置日志设置"""
    # 创建logs目录
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    # 移除默认的sink
    logger.remove()
    
    # 添加控制台输出
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    # 添加文件输出
    logger.add(
        "logs/trade.log",
        rotation="00:00",  # 每天午夜切换文件
        retention="30 days",  # 保留30天的日志
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        encoding='utf-8'
    )
from loguru import logger
import ctypes
import subprocess
import time

def turn_off_monitor():
    """主动关闭显示器"""
    try:
        WM_SYSCOMMAND = 0x0112
        SC_MONITORPOWER = 0xF170
        MONITOR_OFF = 2  # 2 = 关闭显示器, 1 = 低电量模式, -1 = 开启显示器
        
        logger.info("正在尝试关闭显示器...")
        result = ctypes.windll.user32.PostMessageW(None, WM_SYSCOMMAND, SC_MONITORPOWER, MONITOR_OFF)
        if result == 0:
            logger.warning("PostMessageW返回0，可能未成功关闭显示器")
        else:
            logger.info("显示器关闭命令已发送")
        
        # 等待一小段时间确保命令被执行
        time.sleep(1)
    except Exception as e:
        logger.exception("关闭显示器失败")

def set_windows_power_settings():
    """设置Windows电源选项，防止系统休眠但允许显示器息屏"""
    try:
        logger.info("开始设置Windows电源选项...")
        
        # 设置显示器在2分钟不操作后熄屏
        logger.info("设置显示器超时时间...")
        result = subprocess.run("powercfg /change monitor-timeout-ac 2", shell=True, capture_output=True, text=True)
        logger.info(f"AC电源显示器超时设置结果: {result.stdout if result.stdout else result.stderr}")
        
        result = subprocess.run("powercfg /change monitor-timeout-dc 2", shell=True, capture_output=True, text=True)
        logger.info(f"DC电源显示器超时设置结果: {result.stdout if result.stdout else result.stderr}")
        
        # 禁用系统休眠
        logger.info("禁用系统休眠...")
        commands = [
            "powercfg /change standby-timeout-ac 0",
            "powercfg /change standby-timeout-dc 0",
            "powercfg /change hibernate-timeout-ac 0",
            "powercfg /change hibernate-timeout-dc 0"
        ]
        
        for cmd in commands:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            logger.info(f"电源命令 {cmd} 执行结果: {result.stdout if result.stdout else result.stderr}")
        
        # 设置系统不休眠但允许显示器息屏
        logger.info("设置系统保持唤醒状态...")
        ES_CONTINUOUS = 0x80000000
        ES_SYSTEM_REQUIRED = 0x00000001
        
        result = ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
        logger.info(f"系统唤醒状态设置结果: {result}")
        
        logger.info("Windows电源设置已完成")
        
        # 主动关闭显示器
        logger.info("尝试立即关闭显示器...")
        turn_off_monitor()
        
    except Exception as e:
        logger.exception("设置Windows电源选项失败")

def init_power_settings():
    """初始化电源设置"""
    try:
        logger.info("开始初始化电源设置...")
        set_windows_power_settings()
        logger.info("电源设置初始化完成")
    except Exception as e:
        logger.exception("初始化电源设置失败") 
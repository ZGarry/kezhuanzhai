import ctypes
import subprocess
import logging

logger = logging.getLogger(__name__)

def set_windows_power_settings():
    """设置Windows电源选项，防止系统休眠"""
    try:
        # 设置显示器在2分钟不操作后熄屏
        subprocess.call("powercfg /change monitor-timeout-ac 2", shell=True)
        subprocess.call("powercfg /change monitor-timeout-dc 2", shell=True)
        
        # 设置系统不休眠
        ES_CONTINUOUS = 0x80000000
        ES_SYSTEM_REQUIRED = 0x00000001
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
        
        logger.info("Windows电源设置已更新")
    except Exception as e:
        logger.error(f"设置Windows电源选项失败: {e}")
        # 继续运行程序，不中断主要功能

def init_power_settings():
    """初始化电源设置"""
    try:
        set_windows_power_settings()
    except Exception as e:
        logger.warning(f"设置系统电源选项失败，但不影响主程序运行: {e}") 
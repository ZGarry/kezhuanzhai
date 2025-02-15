from loguru import logger
import subprocess
import ctypes

def set_windows_power_settings():
    """设置Windows电源选项:
    1. 显示器1分钟后自动关闭
    2. 禁用系统休眠和睡眠
    3. 保持系统唤醒状态
    """
    try:
        # 设置显示器在1分钟不操作后熄屏
        subprocess.run("powercfg /change monitor-timeout-ac 1", shell=True)
        subprocess.run("powercfg /change monitor-timeout-dc 1", shell=True)
        
        # 禁用系统休眠和睡眠
        commands = [
            "powercfg /change standby-timeout-ac 0",
            "powercfg /change standby-timeout-dc 0",
            "powercfg /change hibernate-timeout-ac 0", 
            "powercfg /change hibernate-timeout-dc 0"
        ]
        
        for cmd in commands:
            subprocess.run(cmd, shell=True)
        
        # 设置系统保持唤醒状态
        ES_CONTINUOUS = 0x80000000
        ES_SYSTEM_REQUIRED = 0x00000001
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
        
        logger.info("电源设置已完成: 1分钟自动息屏,系统不休眠")
        
        # 调用 Windows API 函数来使屏幕关闭
        # ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)

    except Exception as e:
        logger.exception("设置Windows电源选项失败")

def init_power_settings():
    """初始化电源设置"""
    try:
        set_windows_power_settings()
    except Exception as e:
        logger.exception("初始化电源设置失败") 
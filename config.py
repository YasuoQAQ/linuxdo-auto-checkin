"""
配置文件 - LinuxDo 自动签到
"""

import os
import random

class Config:
    """配置类"""
    
    # 基础配置
    USERNAME = os.environ.get("LINUXDO_USERNAME") or os.environ.get("USERNAME")
    PASSWORD = os.environ.get("LINUXDO_PASSWORD") or os.environ.get("PASSWORD")
    
    # 功能开关
    BROWSE_ENABLED = os.environ.get("BROWSE_ENABLED", "true").strip().lower() not in [
        "false", "0", "off"
    ]
    
    # 网络配置
    PROXY_URL = os.environ.get("PROXY_URL")
    TIMEOUT = int(os.environ.get("TIMEOUT", "30"))
    
    # 通知配置
    GOTIFY_URL = os.environ.get("GOTIFY_URL")
    GOTIFY_TOKEN = os.environ.get("GOTIFY_TOKEN")
    SC3_PUSH_KEY = os.environ.get("SC3_PUSH_KEY")
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
    TELEGRAM_USERID = os.environ.get("TELEGRAM_USERID")
    
    # 网站 URL
    HOME_URL = "https://linux.do/"
    LOGIN_URL = "https://linux.do/login"
    CONNECT_URL = "https://connect.linux.do/"
    
    # 浏览器配置
    HEADLESS = os.environ.get("HEADLESS", "true").strip().lower() not in [
        "false", "0", "off"
    ]
    
    # 随机化配置
    CHROME_VERSIONS = [
        "131.0.0.0", "130.0.0.0", "129.0.0.0", "128.0.0.0", "127.0.0.0"
    ]
    
    WINDOW_SIZES = [
        (1366, 768), (1920, 1080), (1440, 900), (1536, 864),
        (1600, 900), (1280, 720), (1024, 768)
    ]
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36"
    ]
    
    # 行为配置
    MIN_SCROLL_DISTANCE = 300
    MAX_SCROLL_DISTANCE = 800
    MIN_SCROLL_COUNT = 5
    MAX_SCROLL_COUNT = 12
    
    MIN_WAIT_TIME = 1.5
    MAX_WAIT_TIME = 4.5
    
    MIN_TOPICS = 5
    MAX_TOPICS = 10
    
    LIKE_PROBABILITY = 0.3  # 点赞概率
    EARLY_EXIT_PROBABILITY = 0.08  # 提前退出概率
    
    @classmethod
    def get_random_chrome_version(cls):
        """获取随机 Chrome 版本"""
        return random.choice(cls.CHROME_VERSIONS)
    
    @classmethod
    def get_random_window_size(cls):
        """获取随机窗口大小"""
        return random.choice(cls.WINDOW_SIZES)
    
    @classmethod
    def get_random_user_agent(cls):
        """获取随机 User-Agent"""
        version = cls.get_random_chrome_version()
        template = random.choice(cls.USER_AGENTS)
        return template.format(version=version)
    
    @classmethod
    def get_platform_identifier(cls):
        """根据系统获取平台标识"""
        from sys import platform
        if platform == "linux" or platform == "linux2":
            return "X11; Linux x86_64"
        elif platform == "darwin":
            return "Macintosh; Intel Mac OS X 10_15_7"
        elif platform == "win32":
            return "Windows NT 10.0; Win64; x64"
        else:
            return "X11; Linux x86_64"
    
    @classmethod
    def validate_config(cls):
        """验证配置"""
        errors = []
        
        if not cls.USERNAME:
            errors.append("缺少用户名配置 (LINUXDO_USERNAME)")
        
        if not cls.PASSWORD:
            errors.append("缺少密码配置 (LINUXDO_PASSWORD)")
        
        if cls.GOTIFY_URL and not cls.GOTIFY_TOKEN:
            errors.append("配置了 GOTIFY_URL 但缺少 GOTIFY_TOKEN")
        
        if cls.GOTIFY_TOKEN and not cls.GOTIFY_URL:
            errors.append("配置了 GOTIFY_TOKEN 但缺少 GOTIFY_URL")
        
        if cls.TELEGRAM_TOKEN and not cls.TELEGRAM_USERID:
            errors.append("配置了 TELEGRAM_TOKEN 但缺少 TELEGRAM_USERID")
        
        if cls.TELEGRAM_USERID and not cls.TELEGRAM_TOKEN:
            errors.append("配置了 TELEGRAM_USERID 但缺少 TELEGRAM_TOKEN")
        
        return errors

"""
日志工具模块
结构化日志配置，按模块分 logger
"""
import logging
import sys
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """JSON 格式日志"""
    # 这是重写方法:重写成这段代码后，每次打日志都会被转成结构化的字典/JSON 格式
    # 每当你在代码里执行任何一句 logger.info(...)、logger.error(...)、logger.warning(...) 时，
    # Python 底层就会自动调用一次这个 format() 方法
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return str(log_entry)


def get_logger(name: str) -> logging.Logger:
    """获取模块 logger"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


# 预定义模块 logger 预定义 5 个模块 logger，各模块按需导入使用
agent_logger = get_logger("agent")        # Agent 核心逻辑
mcp_logger = get_logger("mcp")            # MCP 工具相关
sandbox_logger = get_logger("sandbox")    # 沙箱操作
web_logger = get_logger("web")            # Web API 层
middleware_logger = get_logger("middleware")  # 中间件

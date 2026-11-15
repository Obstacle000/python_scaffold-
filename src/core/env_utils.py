"""
环境变量加载工具
从项目根目录 .env 文件加载环境变量到 os.environ
"""
import os
from pathlib import Path
from dotenv import load_dotenv


def load_env():
    """加载项目根目录的 .env 文件"""
    # 项目根目录：src/../.env
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(env_file, override=True)
    else:
        # 如果不存在 .env，尝试读取 .env.example 作为默认
        example_file = project_root / ".env.example"
        if example_file.exists():
            load_dotenv(example_file, override=False)


def get_env(key: str, default: str = None) -> str:
    """获取字符串环境变量"""
    val = os.getenv(key)
    if val is None or val == "":
        return default
    return val


def get_env_int(key: str, default: int = 0) -> int:
    """获取整数环境变量"""
    val = os.getenv(key)
    if val is None or val == "":
        return default
    try:
        return int(val)
    except ValueError:
        return default


def get_env_bool(key: str, default: bool = False) -> bool:
    """获取布尔环境变量"""
    val = os.getenv(key)
    if val is None or val == "":
        return default
    return val.strip().lower() in ("true", "1", "yes", "y", "on")


# 模块加载时自动加载 .env
load_env()

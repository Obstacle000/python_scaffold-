"""
全局配置模块
LLM、数据库、Redis、Qdrant、MCP 连接参数
风格完全对齐 ERP-AGENT
"""
import os
from src.core.env_utils import get_env, get_env_int, get_env_bool

# ============ LLM 配置 ============
LLM_MODEL = get_env("LLM_MODEL", "deepseek-chat")
LLM_BASE_URL = get_env("LLM_BASE_URL", "https://api.deepseek.com")
# 支持 DEEPSEEK_API_KEY 与通用的 LLM_API_KEY
LLM_API_KEY = get_env("DEEPSEEK_API_KEY", "") or get_env("LLM_API_KEY", "")
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 4096


def get_llm(*, temperature: float | None = None, max_tokens: int = LLM_MAX_TOKENS):
    """获取大模型实例 (兼容 OpenAI / DeepSeek / 通义千问等)."""
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=LLM_MODEL,
        base_url=LLM_BASE_URL,
        api_key=LLM_API_KEY or "sk-placeholder",
        temperature=LLM_TEMPERATURE if temperature is None else temperature,
        max_tokens=max_tokens,
    )


# ============ Embedding 向量配置 ============
EMBEDDING_API_KEY = get_env("EMBEDDING_API_KEY", "") or LLM_API_KEY
EMBEDDING_BASE_URL = get_env("EMBEDDING_BASE_URL", "") or LLM_BASE_URL
EMBEDDING_MODEL = get_env("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIM = get_env_int("EMBEDDING_DIM", 1536)

# ============ 存储与中间件配置 ============
MYSQL_DSN = get_env("MYSQL_DSN", "sqlite+aiosqlite:///./local_app.db")
REDIS_URL = get_env("REDIS_URL", "redis://127.0.0.1:6379/0")
QDRANT_URL = get_env("QDRANT_URL", "http://127.0.0.1:6333")
ES_URL = get_env("ES_URL", "http://127.0.0.1:9200")

# ============ MCP Server 配置 ============
MCP_SERVER_URL = get_env("MCP_SERVER_URL", "http://localhost:9000")
MCP_SSE_URL = f"{MCP_SERVER_URL}/sse"
MCP_HOST = get_env("MCP_HOST", "0.0.0.0")
MCP_PORT = get_env_int("MCP_PORT", 9000)

# ============ Web API 服务配置 ============
APP_NAME = get_env("APP_NAME", "py-ai-framework")
APP_HOST = get_env("APP_HOST", "0.0.0.0")
APP_PORT = get_env_int("APP_PORT", 8000)
DEBUG = get_env_bool("DEBUG", True)
SECRET_KEY = get_env("SECRET_KEY", "your-secret-key-change-in-production")

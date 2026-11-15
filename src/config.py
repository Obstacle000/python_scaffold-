"""全局配置管理模块 (基于 pydantic-settings).

集中管理应用运行期所需的环境变量与配置项，支持自动从项目根目录 `.env` 文件加载。
"""

from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# 项目根目录路径定位 (py项目框架/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """应用全局配置项."""

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # 1. 基础应用配置
    app_name: str = "AI-Project-Framework"
    app_env: str = "dev"  # dev, test, prod
    debug: bool = True
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    secret_key: str = "your-secret-key-change-in-production"

    # 2. LLM 大模型配置 (支持 OpenAI 兼容格式 / DeepSeek / 通义千问等)
    llm_api_key: str = ""
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.7
    llm_timeout: int = 60

    # 3. 向量 Embedding 配置
    embedding_api_key: str = ""
    embedding_base_url: str = ""
    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536

    # 4. 关系型数据库 (MySQL / PostgreSQL / SQLite)
    # 默认使用本地 SQLite 避免强依赖，配置 MYSQL_DSN 后自动切换
    mysql_enabled: bool = False
    mysql_dsn: str = "sqlite+aiosqlite:///./local_app.db"

    # 5. 缓存中间件 (Redis)
    redis_enabled: bool = False
    redis_url: str = "redis://127.0.0.1:6379/0"

    # 6. 向量数据库 (Qdrant)
    qdrant_enabled: bool = False
    qdrant_url: str = "http://127.0.0.1:6333"

    # 7. 搜索引擎 (Elasticsearch)
    es_enabled: bool = False
    es_url: str = "http://127.0.0.1:9200"

    # 8. MCP (Model Context Protocol) 服务配置
    mcp_host: str = "0.0.0.0"
    mcp_port: int = 9000


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """获取缓存的全局配置实例 (单例模式)."""
    return Settings()


# 全局单例配置导出
settings = get_settings()

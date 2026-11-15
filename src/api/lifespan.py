"""FastAPI 应用生命周期管理 (Lifespan).

在应用启动时按需初始化外部资源与连接池，在服务关闭时安全释放连接。
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.clients import (
    database_client_manager,
    redis_client_manager,
    qdrant_client_manager,
    es_client_manager,
    embedding_client_manager,
)
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """全局生命周期钩子."""
    print(f"🚀 正在启动 {settings.app_name} (Env: {settings.app_env})...")

    # 1. 启动阶段：初始化已启用的基础设施
    if settings.mysql_enabled:
        database_client_manager.init()
        print("✅ 关系型数据库客户端已就绪")

    if settings.redis_enabled:
        redis_client_manager.init()
        print("✅ Redis 客户端已就绪")

    if settings.qdrant_enabled:
        qdrant_client_manager.init()
        print("✅ Qdrant 向量客户端已就绪")

    if settings.es_enabled:
        es_client_manager.init()
        print("✅ Elasticsearch 客户端已就绪")

    embedding_client_manager.init()

    yield

    # 2. 停机阶段：安全关闭连接池与释放资源
    print("🛑 正在关闭应用资源连接...")
    await qdrant_client_manager.close()
    await es_client_manager.close()
    await redis_client_manager.close()
    await database_client_manager.close()
    print("✨ 所有资源已安全释放")

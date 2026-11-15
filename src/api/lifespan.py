"""FastAPI 应用生命周期管理 (Lifespan)."""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.clients import (
    database_client_manager,
    redis_client_manager,
    qdrant_client_manager,
    es_client_manager,
    embedding_client_manager,
    llm_client_manager
)
from src.agent.config import APP_NAME


@asynccontextmanager
async def lifespan(app: FastAPI):
    """全局生命周期钩子."""
    print(f"🚀 正在启动 {APP_NAME}...")

    # 初始化数据库与客户端连接
    database_client_manager.init()
    embedding_client_manager.init()  # 触发预热
    redis_client_manager.init()
    es_client_manager.init()
    qdrant_client_manager.init()

    yield

    # 安全关闭连接
    print("🛑 正在关闭应用资源连接...")
    await qdrant_client_manager.close()
    await es_client_manager.close()
    await redis_client_manager.close()
    await database_client_manager.close()
    await llm_client_manager.close()
    await embedding_client_manager.close()
    print("✨ 所有资源已安全释放")

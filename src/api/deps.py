"""FastAPI 依赖注入装配模块 (Dependencies).

集中提供：
1. 基础底层连接（Database Session、Redis、Qdrant、ES、LLM、Embedding）
2. 业务仓储实例（MySQL Repo、Redis Repo、Qdrant Repo、ES Repo）的自动注入。
"""

from collections.abc import AsyncIterator
from typing import Annotated, Any
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from qdrant_client import AsyncQdrantClient
from elasticsearch import AsyncElasticsearch

# 1. 客户端单例
from src.clients import (
    database_client_manager,
    redis_client_manager,
    qdrant_client_manager,
    es_client_manager,
    llm_client_manager,
    embedding_client_manager,
)
from agent.config import EMBEDDING_DIM

# 2. 仓储实现
from src.repo import (
    ExampleMySQLRepository,
    ExampleRedisRepository,
    ExampleQdrantRepository,
    ExampleESRepository,
)


# =====================================================================
# 一、底层客户端与会话装配
# =====================================================================

async def get_db_session() -> AsyncIterator[AsyncSession]:
    """请求级数据库异步会话（请求结束自动释放与提交/回滚）."""
    if database_client_manager.session_factory is None:
        database_client_manager.init()
    assert database_client_manager.session_factory is not None
    async with database_client_manager.session_factory() as session:
        yield session


def get_redis_client() -> Redis | None:
    """获取 Redis 异步客户端单例."""
    if redis_client_manager.client is None:
        redis_client_manager.init()
    return redis_client_manager.client


def get_qdrant_client() -> AsyncQdrantClient | None:
    """获取 Qdrant 客户端单例."""
    if qdrant_client_manager.client is None:
        qdrant_client_manager.init()
    return qdrant_client_manager.client


def get_es_client() -> AsyncElasticsearch | None:
    """获取 Elasticsearch 客户端单例."""
    if es_client_manager.client is None:
        es_client_manager.init()
    return es_client_manager.client


def get_llm() -> Any:
    """获取 LangChain ChatOpenAI 大模型实例."""
    return llm_client_manager.get_llm()


def get_embedding() -> Any:
    """获取向量嵌入模型实例."""
    return embedding_client_manager.client


# 客户端依赖类型标注
DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
RedisDep = Annotated[Redis | None, Depends(get_redis_client)]
QdrantDep = Annotated[AsyncQdrantClient | None, Depends(get_qdrant_client)]
ESDep = Annotated[AsyncElasticsearch | None, Depends(get_es_client)]
LLMDep = Annotated[Any, Depends(get_llm)]
EmbeddingDep = Annotated[Any, Depends(get_embedding)]


# =====================================================================
# 二、业务仓储层 (Repository) 依赖注入装配
# =====================================================================

def get_example_mysql_repo(session: DBSessionDep) -> ExampleMySQLRepository:
    """依赖注入：装配 MySQL 业务数据仓储."""
    return ExampleMySQLRepository(session)


def get_example_redis_repo(client: RedisDep) -> ExampleRedisRepository:
    """依赖注入：装配 Redis 缓存业务仓储."""
    return ExampleRedisRepository(client)


def get_example_qdrant_repo(client: QdrantDep) -> ExampleQdrantRepository:
    """依赖注入：装配 Qdrant 向量检索仓储."""
    return ExampleQdrantRepository(
        client=client,
        collection_name="example_vectors",
        vector_dim=EMBEDDING_DIM,
    )


def get_example_es_repo(client: ESDep) -> ExampleESRepository:
    """依赖注入：装配 Elasticsearch 全文检索仓储."""
    return ExampleESRepository(
        client=client,
        index_name="example_documents",
    )


# 仓储依赖类型标注 (在 Router 或 Service 中直接注解即可完成自动装配)
ExampleMySQLRepoDep = Annotated[ExampleMySQLRepository, Depends(get_example_mysql_repo)]
ExampleRedisRepoDep = Annotated[ExampleRedisRepository, Depends(get_example_redis_repo)]
ExampleQdrantRepoDep = Annotated[ExampleQdrantRepository, Depends(get_example_qdrant_repo)]
ExampleESRepoDep = Annotated[ExampleESRepository, Depends(get_example_es_repo)]

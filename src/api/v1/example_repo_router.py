"""仓储依赖注入使用范例路由 (演示如何在路由中一秒注入各类 Repo)."""

from fastapi import APIRouter
from src.api.deps import (
    ExampleMySQLRepoDep,
    ExampleRedisRepoDep,
    ExampleQdrantRepoDep,
    ExampleESRepoDep,
)
from src.schemas import ApiResponse

router = APIRouter(prefix="/examples", tags=["仓储注入范例"])


@router.get("/redis", summary="演示使用装配好的 Redis Repo")
async def demo_redis(redis_repo: ExampleRedisRepoDep, key: str = "test_key"):
    """直接在参数中声明 `redis_repo: ExampleRedisRepoDep`，FastAPI 自动注入完成."""
    # 写入缓存
    await redis_repo.set_json(key, {"message": "Hello from Redis Repo!", "status": "ok"}, expire_seconds=60)
    # 读取缓存
    cached = await redis_repo.get_json(key)
    return ApiResponse.success(data=cached)


@router.get("/mysql", summary="演示使用装配好的 MySQL Repo")
async def demo_mysql(mysql_repo: ExampleMySQLRepoDep):
    """直接在参数中声明 `mysql_repo: ExampleMySQLRepoDep`，自动获取当前请求 Session."""
    items = await mysql_repo.list_active(skip=0, limit=10)
    return ApiResponse.success(data=[{"id": item.id, "title": item.title} for item in items])


@router.get("/search-vector", summary="演示使用装配好的 Qdrant 向量 Repo")
async def demo_qdrant(qdrant_repo: ExampleQdrantRepoDep):
    """演示向量数据库检索注入."""
    # 假设一个随机或实际向量
    mock_vector = [0.1] * qdrant_repo.vector_dim
    hits = await qdrant_repo.search_similar(query_vector=mock_vector, top_k=3)
    return ApiResponse.success(data=hits)


@router.get("/search-keyword", summary="演示使用装配好的 ES 全文 Repo")
async def demo_es(es_repo: ExampleESRepoDep, keyword: str = "AI"):
    """演示 Elasticsearch BM25 全文检索注入."""
    hits = await es_repo.search_bm25(keyword=keyword, top_k=5)
    return ApiResponse.success(data=hits)

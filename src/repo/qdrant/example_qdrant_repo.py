"""Qdrant 向量数据库仓储示例 (负责知识库/文档向量的存储与语义相似度召回)."""

from typing import Any, Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


class ExampleQdrantRepository:
    """管理向量数据集合的 Qdrant 仓储."""

    def __init__(
        self,
        client: AsyncQdrantClient | None,
        collection_name: str = "example_vectors",
        vector_dim: int = 1536,
    ) -> None:
        self.client = client
        self.collection_name = collection_name
        self.vector_dim = vector_dim

    async def ensure_collection(self) -> None:
        """确保目标向量集合已存在，若不存在则创建 (采用余弦相似度 Cosine)."""
        if self.client is None:
            return
        collections = await self.client.get_collections()
        existing = [c.name for c in collections.collections]
        if self.collection_name not in existing:
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_dim,
                    distance=Distance.COSINE,
                ),
            )

    async def upsert_vector(
        self,
        point_id: str | int,
        vector: list[float],
        payload: dict[str, Any],
    ) -> None:
        """插入或更新单个向量点 (Point)."""
        if self.client is None:
            return
        await self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload,
                )
            ],
        )

    async def search_similar(
        self,
        query_vector: list[float],
        top_k: int = 5,
        score_threshold: float = 0.5,
    ) -> list[dict[str, Any]]:
        """基于向量余弦相似度检索前 K 个最相近的结果."""
        if self.client is None:
            return []

        search_result = await self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k,
            score_threshold=score_threshold,
        )

        return [
            {
                "id": hit.id,
                "score": hit.score,
                "payload": hit.payload,
            }
            for hit in search_result
        ]

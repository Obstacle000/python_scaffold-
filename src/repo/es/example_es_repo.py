"""Elasticsearch 全文检索引擎仓储示例 (负责全文检索、关键字精准匹配与日志记录)."""

from typing import Any, Optional
from elasticsearch import AsyncElasticsearch


class ExampleESRepository:
    """管理文档倒排索引与 BM25 检索的 Elasticsearch 仓储."""

    def __init__(
        self,
        client: AsyncElasticsearch | None,
        index_name: str = "example_documents",
    ) -> None:
        self.client = client
        self.index_name = index_name

    async def ensure_index(self) -> None:
        """确保目标索引存在，若不存在则创建."""
        if self.client is None:
            return
        exists = await self.client.indices.exists(index=self.index_name)
        if not exists:
            await self.client.indices.create(
                index=self.index_name,
                mappings={
                    "properties": {
                        "id": {"type": "keyword"},
                        "title": {"type": "text"},
                        "content": {"type": "text"},
                        "created_at": {"type": "date"},
                    }
                },
            )

    async def index_document(self, doc_id: str, document: dict[str, Any]) -> None:
        """写入或更新单个文档."""
        if self.client is None:
            return
        await self.client.index(
            index=self.index_name,
            id=doc_id,
            document=document,
        )

    async def search_bm25(self, keyword: str, top_k: int = 5) -> list[dict[str, Any]]:
        """基于 BM25 算法执行全文加权多字段检索."""
        if self.client is None:
            return []

        resp = await self.client.search(
            index=self.index_name,
            size=top_k,
            query={
                "multi_match": {
                    "query": keyword,
                    "fields": ["title^2", "content"],
                }
            },
        )

        hits: list[dict[str, Any]] = []
        for item in resp.get("hits", {}).get("hits", []):
            hits.append(
                {
                    "id": item.get("_id"),
                    "score": item.get("_score"),
                    "source": item.get("_source", {}),
                }
            )
        return hits

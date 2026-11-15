"""Elasticsearch 异步客户端管理器."""

from elasticsearch import AsyncElasticsearch
from src.agent.config import ES_URL


class ESClientManager:
    """管理 Elasticsearch 异步客户端生命周期."""

    def __init__(self) -> None:
        self.client: AsyncElasticsearch | None = None

    def init(self, url: str | None = None) -> None:
        if self.client is None:
            self.client = AsyncElasticsearch(hosts=[url or ES_URL])

    async def is_available(self) -> bool:
        if self.client is None:
            return False
        try:
            return bool(await self.client.ping())
        except Exception:
            return False

    async def close(self) -> None:
        if self.client is not None:
            await self.client.close()
            self.client = None


es_client_manager = ESClientManager()

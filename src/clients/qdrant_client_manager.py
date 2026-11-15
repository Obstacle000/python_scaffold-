"""Qdrant 异步向量库客户端管理器."""

from qdrant_client import AsyncQdrantClient
from agent.config import QDRANT_URL


class QdrantClientManager:
    """管理 Qdrant 客户端生命周期."""

    def __init__(self) -> None:
        self.client: AsyncQdrantClient | None = None

    def init(self, url: str | None = None) -> None:
        if self.client is None:
            self.client = AsyncQdrantClient(url=url or QDRANT_URL)

    async def is_available(self) -> bool:
        if self.client is None:
            return False
        try:
            await self.client.get_collections()
            return True
        except Exception:
            return False

    async def close(self) -> None:
        if self.client is not None:
            await self.client.close()
            self.client = None


qdrant_client_manager = QdrantClientManager()

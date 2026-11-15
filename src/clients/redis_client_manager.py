"""Redis 异步连接池管理器."""

from redis.asyncio import Redis
from src.config import settings


class RedisClientManager:
    """管理平台 Redis 异步客户端生命周期."""

    def __init__(self) -> None:
        self.client: Redis | None = None

    def init(self, url: str | None = None) -> None:
        """初始化 Redis 连接池."""
        if not settings.redis_enabled:
            self.client = None
            return
        if self.client is None:
            self.client = Redis.from_url(url or settings.redis_url, decode_responses=True)

    async def is_available(self) -> bool:
        """检测 Redis 服务是否连通."""
        if self.client is None:
            return False
        try:
            return bool(await self.client.ping())
        except Exception:
            return False

    async def close(self) -> None:
        """安全关闭 Redis 客户端."""
        if self.client is not None:
            await self.client.aclose()
            self.client = None


# 全局单例导出
redis_client_manager = RedisClientManager()

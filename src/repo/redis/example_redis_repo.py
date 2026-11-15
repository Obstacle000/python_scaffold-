"""Redis 缓存与键值操作仓储示例."""

import json
from typing import Any, Optional
from redis.asyncio import Redis


class ExampleRedisRepository:
    """管理通用缓存数据的 Redis 仓储."""

    def __init__(self, client: Redis | None, prefix: str = "app:cache:") -> None:
        self.client = client
        self.prefix = prefix

    def _key(self, key: str) -> str:
        """为键拼接统一前缀，避免与其他业务键冲突."""
        return f"{self.prefix}{key}"

    async def get_json(self, key: str) -> Optional[Any]:
        """从 Redis 获取数据并自动反序列化为字典/列表."""
        if self.client is None:
            return None
        raw = await self.client.get(self._key(key))
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except Exception:
            return raw

    async def set_json(self, key: str, value: Any, expire_seconds: int = 3600) -> bool:
        """将数据序列化为 JSON 字符串并存入 Redis (带 TTL)."""
        if self.client is None:
            return False
        payload = json.dumps(value, ensure_ascii=False)
        return bool(await self.client.set(self._key(key), payload, ex=expire_seconds))

    async def delete(self, key: str) -> bool:
        """删除指定缓存键."""
        if self.client is None:
            return False
        return bool(await self.client.delete(self._key(key)))

    async def exists(self, key: str) -> bool:
        """检查键是否存在."""
        if self.client is None:
            return False
        return bool(await self.client.exists(self._key(key)))

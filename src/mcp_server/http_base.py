"""通用 HTTP 客户端模块 (单例模式).

基于 httpx.AsyncClient 实现连接池管理与复用，适合在 MCP 工具内部安全高效地调用第三方 API。
"""

import httpx
from typing import Any, Optional
from agent.config import settings


class BaseHttpClient:
    """通用外部接口 HTTP 异步客户端单例."""

    _instance: Optional["BaseHttpClient"] = None
    _client: Optional[httpx.AsyncClient] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=ERP_BASE_URL,
                timeout=httpx.Timeout(HTTP_TIMEOUT),
                limits=httpx.Limits(
                    max_connections=HTTP_MAX_CONNECTIONS,
                    max_keepalive_connections=10,
                ),
                headers={"Content-Type": "application/json"},
            )
        return self._client

    async def get(self, url: str, params: Optional[dict] = None, headers: Optional[dict] = None) -> Any:
        """发送异步 GET 请求."""
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        response = await self.client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    async def post(self, url: str, json_data: Optional[dict] = None, headers: Optional[dict] = None) -> Any:
        """发送异步 POST 请求."""
        response = await self.client.post(url, json=json_data, headers=headers)
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        """关闭客户端释放连接池."""
        if self._client is not None and not self._client.is_closed:
            await self._client.aclose()
            self._client = None


# 全局单例导出
http_client = BaseHttpClient()

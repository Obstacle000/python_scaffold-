"""Embedding 向量模型客户端管理器."""

import inspect
from typing import Any
from src.agent.config import (
    EMBEDDING_API_KEY,
    EMBEDDING_BASE_URL,
    EMBEDDING_MODEL,
    EMBEDDING_DIM,
)


class EmbeddingClientManager:
    """管理向量嵌入模型客户端生命周期."""

    def __init__(self) -> None:
        self.dim = EMBEDDING_DIM
        self.model = EMBEDDING_MODEL
        self.api_key = EMBEDDING_API_KEY
        self.base_url = EMBEDDING_BASE_URL
        self._client: Any = None

    @property
    def client(self) -> Any:
        """获取或懒加载 OpenAIEmbeddings 客户端."""
        if self._client is None:
            from langchain_openai import OpenAIEmbeddings

            kwargs: dict[str, Any] = {
                "model": self.model,
                "api_key": self.api_key or "sk-placeholder",
            }
            if self.base_url:
                kwargs["base_url"] = self.base_url
            self._client = OpenAIEmbeddings(**kwargs)
        return self._client

    def init(self) -> None:
        """提前构造 embedding 客户端（构造不建立连接，不是真正的预热）."""
        _ = self.client

    async def close(self) -> None:
        """关闭底层 openai SDK 连接池."""
        client, self._client = self._client, None
        if client is None:
            return
        # OpenAIEmbeddings 的 SDK client 字段名与 ChatOpenAI 不同
        for attr in ("async_client", "client"):
            sdk = getattr(client, attr, None)
            if sdk is None:
                continue
            result = sdk.close()
            if inspect.isawaitable(result):
                await result

    def has_valid_key(self) -> bool:
        """判断是否配置了有效密钥."""
        key = (self.api_key or "").strip()
        return bool(key) and not key.startswith("sk-your-") and key != "sk-placeholder"

    async def embed_text(self, text: str) -> list[float]:
        """将单个文本编码为高维向量."""
        return await self.client.aembed_query(text)

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """批量编码多个文本文档."""
        return await self.client.aembed_documents(texts)


# 全局单例导出
embedding_client_manager = EmbeddingClientManager()

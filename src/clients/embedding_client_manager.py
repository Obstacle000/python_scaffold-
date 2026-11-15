"""Embedding 向量模型客户端管理器."""

from typing import Any
from agent.config import (
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

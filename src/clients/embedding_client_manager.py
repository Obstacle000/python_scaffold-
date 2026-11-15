"""Embedding 向量模型客户端管理器 (单例与延迟加载模式)."""

from dataclasses import dataclass
from typing import Any
from src.config import settings


@dataclass
class EmbeddingConfig:
    dim: int
    model: str
    api_key: str
    base_url: str


class EmbeddingClientManager:
    """管理向量嵌入模型客户端生命周期."""

    def __init__(self) -> None:
        self.config = EmbeddingConfig(
            dim=settings.embedding_dim,
            model=settings.embedding_model,
            api_key=settings.embedding_api_key or settings.llm_api_key,
            base_url=settings.embedding_base_url or settings.llm_base_url,
        )
        self._client: Any = None

    def init(self) -> None:
        """重新从全局 settings 同步配置."""
        self.config = EmbeddingConfig(
            dim=settings.embedding_dim,
            model=settings.embedding_model,
            api_key=settings.embedding_api_key or settings.llm_api_key,
            base_url=settings.embedding_base_url or settings.llm_base_url,
        )

    @property
    def client(self) -> Any:
        """获取或懒加载 OpenAIEmbeddings 客户端."""
        if self._client is None:
            from langchain_openai import OpenAIEmbeddings

            kwargs: dict[str, Any] = {
                "model": self.config.model,
                "api_key": self.config.api_key or "sk-placeholder",
            }
            if self.config.base_url:
                kwargs["base_url"] = self.config.base_url
            self._client = OpenAIEmbeddings(**kwargs)
        return self._client

    def has_valid_key(self) -> bool:
        """判断是否配置了有效密钥."""
        key = (self.config.api_key or "").strip()
        return bool(key) and not key.startswith("sk-your-") and key != "sk-placeholder"

    async def embed_text(self, text: str) -> list[float]:
        """将单个文本编码为高维向量."""
        return await self.client.aembed_query(text)

    async def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """批量编码多个文本文档."""
        return await self.client.aembed_documents(texts)


# 全局单例导出
embedding_client_manager = EmbeddingClientManager()

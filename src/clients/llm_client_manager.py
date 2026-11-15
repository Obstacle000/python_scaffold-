"""LLM 大模型客户端管理器 (单例与延迟加载模式).

支持通过 LangChain ChatOpenAI 统一接入任何兼容 OpenAI 规范的 API
(如 OpenAI、DeepSeek、通义千问 Qwen、Moonshot、Ollama 等)。
"""

from typing import Any
from src.config import settings


class LLMClientManager:
    """管理大模型客户端生命周期，按需创建与复用."""

    def __init__(self) -> None:
        self._cached_cls: Any = None

    def has_valid_key(self) -> bool:
        """检查是否配置了有效的 API Key."""
        key = (settings.llm_api_key or "").strip()
        return bool(key) and not key.startswith("sk-your-") and key != "sk-placeholder"

    def get_llm(self, model: str | None = None, temperature: float | None = None) -> Any:
        """获取 ChatOpenAI 实例.

        Args:
            model: 覆盖默认模型名称
            temperature: 覆盖默认采样温度
        """
        if self._cached_cls is None:
            from langchain_openai import ChatOpenAI
            self._cached_cls = ChatOpenAI

        return self._cached_cls(
            api_key=settings.llm_api_key or "sk-placeholder",
            base_url=settings.llm_base_url,
            model=model or settings.llm_model,
            temperature=settings.llm_temperature if temperature is None else temperature,
            timeout=settings.llm_timeout,
        )


# 全局单例导出
llm_client_manager = LLMClientManager()

"""LLM 大模型客户端管理器 (单例与延迟加载模式)."""

from typing import Any
from agent.config import get_llm, LLM_API_KEY


class LLMClientManager:
    """管理大模型客户端生命周期."""

    def has_valid_key(self) -> bool:
        """检查是否配置了有效的 API Key."""
        key = (LLM_API_KEY or "").strip()
        return bool(key) and not key.startswith("sk-your-") and key != "sk-placeholder"

    def get_llm(self, temperature: float | None = None) -> Any:
        """获取大模型实例."""
        return get_llm(temperature=temperature)


# 全局单例导出
llm_client_manager = LLMClientManager()

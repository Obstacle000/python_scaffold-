"""LLM 大模型客户端管理器（按温度缓存的单例池 + 延迟加载）."""

import inspect
from typing import Any

from src.agent.config import LLM_API_KEY, LLM_TEMPERATURE, get_llm


class LLMClientManager:
    """管理大模型客户端生命周期：首次使用时创建，之后复用，退出时释放."""

    def __init__(self) -> None:
        # key = 生效温度，value = 该温度下复用的 ChatOpenAI 实例
        self._clients: dict[float, Any] = {}

    def has_valid_key(self) -> bool:
        """检查是否配置了有效的 API Key."""
        key = (LLM_API_KEY or "").strip()
        return bool(key) and not key.startswith("sk-your-") and key != "sk-placeholder"

    def get_llm(self, temperature: float | None = None) -> Any:
        """获取（或首次创建）指定温度下的大模型单例."""
        key = LLM_TEMPERATURE if temperature is None else round(float(temperature), 2)
        client = self._clients.get(key)
        if client is None:
            client = get_llm(temperature=key)   # 注意 config.get_llm 是关键字参数
            self._clients[key] = client
        return client

    async def close(self) -> None:
        """关闭底层 openai SDK 连接池."""
        for client in self._clients.values():
            for attr in ("root_async_client", "root_client"):
                sdk = getattr(client, attr, None)
                if sdk is None:
                    continue
                result = sdk.close()
                if inspect.isawaitable(result):
                    await result
        self._clients.clear()


# 全局单例导出
llm_client_manager = LLMClientManager()
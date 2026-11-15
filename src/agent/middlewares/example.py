"""
中间件
"""
import threading
from typing import Any, Dict, Optional

from langchain.agents.middleware import AgentMiddleware, Runtime
from ..log_utils import middleware_logger
from ..schema import ProcurementContext


class ExampleMiddleware(AgentMiddleware):
    """
    实例中间件
    """

    def __init__(self):
        self._lock = threading.Lock()
        self.tools = []

    @property
    def name(self) -> str:
        return "ExampleMiddleware"

    def before_agent(self, state: Any, runtime: Runtime) -> dict[str, Any] | None:
        """在 Agent 执行前注入用户上下文"""

        return None

    def after_agent(self, state: Any, runtime: Runtime) -> dict[str, Any] | None:
        """Agent 执行后可更新上下文（如新发现的偏好）"""
        return None

    # ============================================================
    # 上下文管理
    # ============================================================

    def update_context(
        self,
        thread_id: str = "",
    ):
        """
        更新用户上下文（新请求时调用）

        Args:
            thread_id: 会话线程ID（用于隔离存储）
        """
        with self._lock:
            if thread_id:
                pass
            else:
                pass


    d

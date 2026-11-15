"""
子Agent中间件工厂（Harness 架构 — 完整中间件栈）
节点编排不需要
"""
from pathlib import Path
from deepagents.middleware import SummarizationToolMiddleware

from .middlewares.example import ContextInjectionMiddleware
from .middlewares.skills_sync import SkillsSyncMiddleware
from .middlewares.sandbox_breaker import SandboxCircuitBreakerMiddleware
from .middlewares.tools_summarization import ToolsSummarizationMiddleware
from .schema import ProcurementContext


# 获取当前文件所在目录的上一级目录的上一级目录的skills目录的绝对路径。
SKILLS_DIR = Path(__file__).parent.parent / "skills"


def example_middleware() -> list:
    """
    实例中间件
    """


    return




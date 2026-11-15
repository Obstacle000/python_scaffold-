"""MCP Server 独立启动入口.

支持基于 FastMCP 注册工具集，并通过 SSE 或 STDIO 协议与 Claude Desktop / Cursor / IDE 联动。
"""

import sys
import os
from pathlib import Path

# 确保项目根目录在 sys.path 中，支持直接以脚本运行
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastmcp import FastMCP
from src.mcp_server.server_config import MCP_HOST, MCP_PORT
from src.mcp_server.tools import register_example_tools

# 1. 创建 MCP Server 实例
mcp = FastMCP(
    name="AI-Project-MCP-Server",
    instructions="通用 AI 扩展工具服务，提供系统实用工具支持。",
)

# 2. 注册工具集合
register_example_tools(mcp)


def run_mcp_server(transport: str = "sse"):
    """启动 MCP Server."""
    print(f"🚀 Starting MCP Server on {MCP_HOST}:{MCP_PORT} (Transport: {transport})")
    mcp.run(transport=transport, host=MCP_HOST, port=MCP_PORT)


if __name__ == "__main__":
    run_mcp_server(transport="sse")

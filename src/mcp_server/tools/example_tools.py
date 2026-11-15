"""示例 MCP 工具模块 (供参考扩展).

通过在函数上添加 `@mcp.tool()` 装饰器，即可自动将 Python 业务逻辑暴露给大模型作为外部工具调用。
"""

from fastmcp import FastMCP
from ..http_base import http_client


def register_example_tools(mcp: FastMCP) -> None:
    """注册通用示例工具集到 MCP Server."""

    @mcp.tool()
    async def query(name: str) -> str:
        """实例工具。

        Args:
            name: 实例参数

        Returns:
            示例返回
        """
        result = await http_client.get("/api/...", params={"name": name})
        return json.dumps(result, ensure_ascii=False, indent=2)

    @mcp.tool()
    async def get_current_time(timezone_name: str = "Asia/Shanghai") -> str:
        """获取指定时区的当前系统准确时间。

        Args:
            timezone_name: 时区名称，例如 'Asia/Shanghai' 或 'UTC'

        Returns:
            格式化后的当前时间字符串
        """
        from datetime import datetime
        import zoneinfo

        try:
            tz = zoneinfo.ZoneInfo(timezone_name)
            now = datetime.now(tz)
            return f"当前时间 ({timezone_name}): {now.strftime('%Y-%m-%d %H:%M:%S')}"
        except Exception:
            return f"当前时间 (本地系统): {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    @mcp.tool()
    async def calculate(expression: str) -> str:
        """安全计算数学算术表达式结果。

        Args:
            expression: 简单算式，例如 '125 * 8 + 35'

        Returns:
            计算结果
        """
        # 注意：生产环境中建议使用 ast.literal_eval 或 sympy 解析数学运算
        import math
        allowed_names = {"math": math, "abs": abs, "round": round, "min": min, "max": max}
        try:
            code = compile(expression, "<string>", "eval")
            for name in code.co_names:
                if name not in allowed_names:
                    return f"错误: 不允许使用非法标识符 '{name}'"
            result = eval(code, {"__builtins__": {}}, allowed_names)
            return f"计算结果: {result}"
        except Exception as e:
            return f"计算失败: {str(e)}"

"""项目全局统一启动入口.

支持通过命令行参数快速启动 FastAPI 服务或 MCP Server：
- 启动 Web API: python main.py
- 启动 MCP Server: python main.py --mcp
"""

import argparse


def main():
    parser = argparse.ArgumentParser(description="AI 项目开发框架启动器")
    parser.add_argument(
        "--mcp",
        action="store_true",
        help="以 MCP Server 模式启动 (默认启动 FastAPI Web 服务)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="覆盖启动监听端口",
    )
    args = parser.parse_args()

    if args.mcp:
        from src.mcp_server.server_main import run_mcp_server
        run_mcp_server()
    else:
        import uvicorn
        from src.agent.config import APP_HOST, APP_PORT, DEBUG

        port = args.port or APP_PORT
        print(f"🌟 启动 FastAPI 服务: http://{APP_HOST}:{port}")
        print(f"📖 交互式文档: http://127.0.0.1:{port}/docs")
        uvicorn.run(
            "src.main:app",
            host=APP_HOST,
            port=port,
            reload=DEBUG,
        )


if __name__ == "__main__":
    main()

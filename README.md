# Python + AI 大模型开发框架脚手架 (AI Project Framework)

一套标准化、模块化、高可扩展的现代 Python AI 应用开发骨架。集成 **FastAPI Web 服务**、**MCP (Model Context Protocol) 工具服务**、**LangChain / OpenAI 兼容生态**与**基础设施连接池单例**。

---

## 📁 目录结构与分层规范

```text
py项目框架/
├── .env.example              # 环境变量配置模板
├── .gitignore                # Git 忽略规则
├── requirements.txt          # 项目核心依赖清单
├── main.py                   # 全局统一启动器 (支持启动 Web API 或 MCP)
└── src/                      # 核心源码目录
    ├── __init__.py
    ├── config.py             # 全局配置中心 (基于 pydantic-settings，读取 .env)
    ├── exceptions.py         # 统一业务异常与错误码体系 (AppError)
    ├── main.py               # FastAPI 主应用 (CORS、全局异常捕获、生命周期)
    │
    ├── api/                  # RESTful API 路由与接口层
    │   ├── deps.py           # 依赖注入装配 (数据库 Session、Redis、LLM 等)
    │   ├── lifespan.py       # 异步生命周期钩子 (优雅启动/释放连接池)
    │   └── v1/               # 版本化路由目录
    │       ├── router.py     # v1 路由总挂载点
    │       └── chat_router.py# 示例接口 (普通问答 / SSE 流式打字机问答)
    │
    ├── clients/              # 基础设施连接池客户端 (单例模式 + 延迟加载)
    │   ├── llm_client_manager.py       # 大模型客户端 (兼容 OpenAI/DeepSeek/Qwen)
    │   ├── embedding_client_manager.py # 向量嵌入客户端
    │   ├── mysql_client_manager.py     # 关系型数据库连接池 (MySQL / SQLite)
    │   ├── redis_client_manager.py     # Redis 异步连接池
    │   ├── qdrant_client_manager.py    # Qdrant 向量数据库连接池
    │   └── es_client_manager.py        # Elasticsearch 异步客户端
    │
    ├── mcp_server/           # MCP (Model Context Protocol) 服务模块
    │   ├── server_config.py  # MCP 服务端口与配置
    │   ├── server_main.py    # MCP 服务端启动入口 (FastMCP)
    │   ├── http_base.py      # 通用外部 HTTP 调用客户端单例
    │   └── tools/            # 自定义 AI 工具集合
    │       └── example_tools.py # 示例 MCP 工具注册模板 (@mcp.tool)
    │
    ├── models/               # 数据表 ORM 持久化模型 (SQLAlchemy)
    │   └── base.py           # Base 声明基类与审计字段 Mixin (id, created_at...)
    │
    ├── repo/                 # 数据访问仓储层 (Repository Pattern)
    │   ├── base_repo.py      # 泛型异步 CRUD 仓储基类 (BaseRepository[T])
    │   ├── mysql/            # MySQL 仓储 (ExampleMySQLRepository)
    │   ├── redis/            # Redis 缓存仓储 (ExampleRedisRepository)
    │   ├── qdrant/           # Qdrant 向量仓储 (ExampleQdrantRepository)
    │   └── es/               # Elasticsearch 全文检索仓储 (ExampleESRepository)
    │
    ├── schemas/              # Pydantic 数据传输模型 (入参、出参、响应包装)
    │   ├── common.py         # 统一响应包装 ApiResponse[T]、分页 PageResult
    │   └── example_schema.py # 示例交互 Schema
    │
    ├── service/              # 核心业务逻辑服务层
    │   └── base_service.py   # 业务服务基类
    │
    ├── agent/                # AI Agent 智能体工作流 (LangGraph / 多智能体流程)
    │   └── prompts/          # 提示词工程模板
    │
    ├── skills/               # 领域专用技能与工具插件
    └── core/                 # 底层系统与基础设施工具
```

---

## 🚀 快速开始

### 1. 准备环境与安装依赖
```bash
python -m venv .venv
# Windows 激活
.venv\Scripts\activate
# Linux/macOS 激活
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. 配置环境变量
复制 `.env.example` 为 `.env`，并填入你的大模型 API Key：
```bash
cp .env.example .env
```
修改 `.env` 中的大模型配置（支持 DeepSeek、OpenAI、月之暗面、通义千问等）：
```env
LLM_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
```

### 3. 启动服务

* **方式 A：启动 Web API 服务（FastAPI）**
  ```bash
  python main.py
  ```
  启动后访问：
  * API 首页健康检查：`http://127.0.0.1:8000/health`
  * Swagger 交互式文档：`http://127.0.0.1:8000/docs`

* **方式 B：启动 MCP Server（供 Claude Desktop / Cursor 调用）**
  ```bash
  python main.py --mcp
  ```
  启动后将在 `0.0.0.0:9000` 监听 SSE 协议。

---

## 💡 开发指南：如何扩展新业务？

### 1. 添加一个新的 Web API 接口
1. 在 `src/schemas/` 中定义请求和响应的 Pydantic 模型；
2. 在 `src/service/` 中编写核心业务逻辑；
3. 在 `src/api/v1/` 中编写路由函数，通过 `Depends` 自动注入数据库或 LLM；
4. 在 `src/api/v1/router.py` 中挂载该路由。

### 2. 添加一个新的 MCP 工具给 AI 使用
打开 `src/mcp_server/tools/`，写一个带类型注解与 Docstring 的 Python 函数，加注 `@mcp.tool()` 即可：
```python
@mcp.tool()
async def search_user(user_id: int) -> str:
    """根据用户 ID 查询用户信息。"""
    return f"用户 {user_id} 状态正常"
```
FastMCP 会自动将注释和参数反射成大模型能够理解的 JSON Schema！

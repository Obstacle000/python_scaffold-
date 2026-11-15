"""FastAPI 应用核心主入口.

配置 CORS 中间件、统一全局业务异常处理、挂载生命周期及业务路由。
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.lifespan import lifespan
from src.api.v1.router import api_v1_router
from src.config import settings
from src.exceptions import AppError

# 创建 FastAPI 实例
app = FastAPI(
    title=settings.app_name,
    description="现代化 Python + AI 大模型开发框架脚手架",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# 跨域配置 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局业务异常捕获处理 (统一返回格式)
@app.exception_handler(AppError)
async def handle_app_error(_request: Request, exc: AppError) -> JSONResponse:
    """捕获自定义业务异常，返回标准化错误 JSON."""
    return JSONResponse(
        status_code=exc.http_status,
        content={
            "code": exc.http_status,
            "error_code": exc.error_code,
            "message": exc.message,
            "data": None,
        },
    )


@app.exception_handler(Exception)
async def handle_unexpected_error(_request: Request, exc: Exception) -> JSONResponse:
    """兜底捕获未处理的运行时异常，防止信息泄露."""
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": str(exc) if settings.debug else "服务器内部错误，请稍后重试",
            "data": None,
        },
    )


# 系统基础路由
@app.get("/health", tags=["系统监控"])
async def health_check() -> dict[str, str]:
    """服务健康检查接口."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "environment": settings.app_env,
    }


# 挂载业务路由
app.include_router(api_v1_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )

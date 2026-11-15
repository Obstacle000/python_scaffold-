"""API v1 统一路由聚合入口."""

from fastapi import APIRouter
from .chat_router import router as chat_router
from .example_repo_router import router as example_repo_router

api_v1_router = APIRouter(prefix="/api/v1")

# 挂载子路由
api_v1_router.include_router(chat_router)
api_v1_router.include_router(example_repo_router)

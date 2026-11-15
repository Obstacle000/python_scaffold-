"""通用的数据传输模型（API 响应包装、分页等）."""

from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """统一 API 响应包装模型."""

    code: int = Field(default=200, description="业务状态码，200 表示成功")
    message: str = Field(default="success", description="提示信息")
    data: Optional[T] = Field(default=None, description="响应数据负载")

    @classmethod
    def success(cls, data: Optional[T] = None, message: str = "success") -> "ApiResponse[T]":
        """构建成功响应."""
        return cls(code=200, message=message, data=data)

    @classmethod
    def error(cls, code: int = 400, message: str = "error", data: Optional[Any] = None) -> "ApiResponse[Any]":
        """构建失败响应."""
        return cls(code=code, message=message, data=data)


class PageQuery(BaseModel):
    """通用分页查询入参."""

    page: int = Field(default=1, ge=1, description="当前页码，从 1 开始")
    page_size: int = Field(default=10, ge=1, le=100, description="每页条数")


class PageResult(BaseModel, Generic[T]):
    """通用分页结果模型."""

    items: list[T] = Field(default_factory=list, description="当前页数据列表")
    total: int = Field(default=0, description="数据总条数")
    page: int = Field(default=1, description="当前页码")
    page_size: int = Field(default=10, description="每页条数")
    total_pages: int = Field(default=0, description="总页数")

"""框架示例数据模型 (供业务开发参考)."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """AI 对话请求入参."""

    prompt: str = Field(..., min_length=1, description="用户提问内容")
    temperature: float | None = Field(default=None, ge=0.0, le=2.0, description="采样温度")
    stream: bool = Field(default=False, description="是否以流式输出返回")


class ChatResponse(BaseModel):
    """AI 对话响应数据."""

    content: str = Field(..., description="大模型回复文本")
    model: str = Field(..., description="实际调用的模型名称")

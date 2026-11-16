"""示例路由：AI 智能对话接口."""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.api.deps import LLMDep
from src.schemas import ApiResponse, ChatRequest, ChatResponse
from src.agent.config import LLM_MODEL

router = APIRouter(prefix="/chat", tags=["AI 对话示例"])

# 可以新建一个工具类
def _format_sse(event: str, payload: dict[str, Any]) -> str:
    return f"event: {event}\ndata: {json.dumps(payload, ensure_ascii=False)}\n\n"

@router.post("", response_model=ApiResponse[ChatResponse], summary="普通单次对话")
async def chat_completion(request: ChatRequest, llm_mgr: LLMDep):
    """调用大模型进行文本对话交互."""
    # 温度由 LLMClientManager 按值缓存，这里拿到的是对应温度下的单例
    llm = llm_mgr.get_llm(request.temperature)
    # 调用大模型 (LangChain ainvoke)
    response = await llm.ainvoke(request.prompt)

    return ApiResponse.success(
        data=ChatResponse(
            content=str(response.content),
            model=LLM_MODEL,
        )
    )


@router.post("/stream", summary="流式打字机效果对话")
async def chat_stream(request: ChatRequest, llm_mgr: LLMDep):
    """以流式输出方式返回大模型生成的文本 (SSE / Transfer-Encoding: chunked)."""
    llm = llm_mgr.get_llm(request.temperature)

    async def event_generator():
        async for chunk in llm.astream(request.prompt):
            if chunk.content:
                yield _format_sse("token", json.loads(chunk.content))

    return StreamingResponse(event_generator(), media_type="text/plain; charset=utf-8")

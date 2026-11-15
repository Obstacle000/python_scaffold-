"""示例路由：AI 智能对话接口."""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.api.deps import LLMDep
from src.schemas import ApiResponse, ChatRequest, ChatResponse
from agent.config import LLM_MODEL

router = APIRouter(prefix="/chat", tags=["AI 对话示例"])


@router.post("", response_model=ApiResponse[ChatResponse], summary="普通单次对话")
async def chat_completion(request: ChatRequest, llm: LLMDep):
    """调用大模型进行文本对话交互."""
    # 如果指定了温度，按需调整
    active_llm = llm if request.temperature is None else llm.with_config({"temperature": request.temperature})

    # 调用大模型 (LangChain ainvoke)
    response = await active_llm.ainvoke(request.prompt)

    return ApiResponse.success(
        data=ChatResponse(
            content=str(response.content),
            model=LLM_MODEL,
        )
    )


@router.post("/stream", summary="流式打字机效果对话")
async def chat_stream(request: ChatRequest, llm: LLMDep):
    """以流式输出方式返回大模型生成的文本 (SSE / Transfer-Encoding: chunked)."""

    async def event_generator():
        async for chunk in llm.astream(request.prompt):
            if chunk.content:
                yield str(chunk.content)

    return StreamingResponse(event_generator(), media_type="text/plain; charset=utf-8")

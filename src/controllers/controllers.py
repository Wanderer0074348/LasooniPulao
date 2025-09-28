from fastapi import APIRouter, HTTPException

from src.app.services import get_llm_response
from src.models.models import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response = await get_llm_response(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error conversing with the llm!!!\n Error: {e}"
        )

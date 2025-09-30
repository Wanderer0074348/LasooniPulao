from fastapi import APIRouter, HTTPException

from src.app.services import create_new_session_id, get_llm_response
from src.models.models import ChatRequest, ChatResponse, SessionResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.session_id:
        return HTTPException(status_code=400, detail="session_id needed mate")
    try:
        response = await get_llm_response(request.message, request.session_id)
        return ChatResponse(response=response, session_id=request.session_id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error conversing with the llm!!!\n Error: {e}"
        )


@router.post("/sessions", response_model=SessionResponse)
async def session_endpoint():
    try:
        session_id = await create_new_session_id()
        return SessionResponse(session_id=session_id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unable to create sessionID\n Error: {e}"
        )

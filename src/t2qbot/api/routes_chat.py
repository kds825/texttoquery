from fastapi import APIRouter, HTTPException
from t2qbot.domain.schemas import ChatRequest, ChatResponse
from t2qbot.services.chat_service import handle

router = APIRouter()

@router.post("/chat", response_model= ChatResponse)
async def chat(req: ChatRequest):
    try:
        sql, rows = await handle(req.message)
        return ChatResponse(sql=sql, rows=rows)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")
    
from pydantic import BaseModel
from typing import Any, Dict, List

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    sql : str
    rows: List[Dict[str, Any]]
    
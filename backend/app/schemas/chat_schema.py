"""
Chat request and response schemas
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None
    system_prompt: Optional[str] = None


class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    sources: List[str] = []
    metadata: Dict[str, Any] = {}

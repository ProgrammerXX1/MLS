from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Literal

class ChatLogItem(BaseModel):
    request_text: str
    response_text: str
    timestamp: datetime
    latency_ms: int
    chat_id: int

    class Config:
        from_attributes = True

class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    title: Optional[str] = Field(None, max_length=100)
    model: Optional[str] = None
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = 1024
    stream: Optional[bool] = False
    response_format: Optional[str] = "text"
    moderation: Optional[bool] = False
    top_p: Optional[float] = 0.75
    seed: Optional[str] = None
    stop: Optional[str] = None

class ChatCreate(BaseModel):
    title: Optional[str] = Field("Новый чат", max_length=100)
    status: str = Field("Draft", max_length=20)

class ChatUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, max_length=20)

class ChatResponse(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    request_text: str
    response_text: str
    latency_ms: int
    timestamp: Optional[datetime] = None
    chat_id: Optional[int] = None

    class Config:
        from_attributes = True

class ChatOut(BaseModel):
    id: int
    title: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatHistoryItem(BaseModel):
    question: str
    answer: str

class ChatLogOut(BaseModel):
    created: str
    model: str
    apiKey: str
    code: int
    ttft: str
    latency: str
    inputTokens: int
    outputTokens: int
    audioSeconds: str
    requestId: str
    error: str
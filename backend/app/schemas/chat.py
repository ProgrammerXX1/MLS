from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Literal

class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = None
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = 1024
    stream: Optional[bool] = False
    response_format: Optional[str] = "text"
    moderation: Optional[bool] = False
    top_p: Optional[float] = 0.75
    seed: Optional[str] = None
    stop: Optional[str] = None

class MessageResponse(BaseModel):
    request_text: str
    response_text: str
    latency_ms: int
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True

class ChatLogItem(BaseModel):
    created: datetime
    model: str
    api_key: str
    code: int
    ttft_ms: float
    latency: float
    input_tokens: int
    output_tokens: int
    audio_seconds: str
    request_id: str
    error: Optional[str]

    class Config:
        from_attributes = True


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

class ChatHistoryItem(BaseModel):
    question: str
    answer: str

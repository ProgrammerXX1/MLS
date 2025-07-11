# schemas/api_keys.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class APIKeyOut(BaseModel):
    id: int
    key: str
    user_id: int
    created_at: datetime

    last_used_at: Optional[datetime] = None
    usage_24h: Optional[int] = None  # временно допускаем None

    class Config:
        from_attributes = True

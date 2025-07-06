# schemas/api_keys.py
from pydantic import BaseModel
from datetime import datetime

class APIKeyOut(BaseModel):
    id: int
    key: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

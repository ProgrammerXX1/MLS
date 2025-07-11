# routes/admin_logs.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.db.models import ChatLog
from uuid import uuid4
from datetime import datetime
from app.schemas.chat import ChatLogOut

router = APIRouter()

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from uuid import uuid4

router = APIRouter()

@router.get("/dash/log")
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(ChatLog).order_by(ChatLog.timestamp.desc()).limit(500).all()

    def safe_model(api_key: str, model: Optional[str]) -> str:
        return model or ("llama-3" if api_key else "unknown-model")

    return [
        {
            "created": log.timestamp.strftime('%d.%m.%Y, %H:%M:%S'),
            "model": safe_model(log.api_key, log.model_name),
            "apiKey": log.api_key or "",
            "code": 200 if log.status == "success" else 500,
            "ttft": f"{(log.latency_ms or 100) / 1000:.3f}",
            "latency": f"{(log.latency_ms or 100) / 1000:.3f}",
            "inputTokens": len(log.request_text.split()),
            "outputTokens": len(log.response_text.split()),
            "audioSeconds": "-",
            "requestId": f"req_{uuid4().hex[:8]}",
            "error": "-" if log.status == "success" else "Internal error"
        }
        for log in logs
    ]


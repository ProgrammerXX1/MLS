from uuid import uuid4
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.db.models import ChatLog
from typing import Optional
router = APIRouter()

@router.get("/dash/log")
def get_logs(db: Session = Depends(get_db)):
    logs = db.query(ChatLog).order_by(ChatLog.timestamp.desc()).limit(500).all()

    def safe_model(api_key: str, model: Optional[str]) -> str:
        return model or ("llama-3" if api_key else "unknown-model")

    return [
        {
            "created": log.timestamp.strftime('%d.%m.%Y, %H:%M:%S') if log.timestamp else "-",
            "model": safe_model(log.api_key, log.model_name),
            "apiKey": log.api_key or "",
            "code": log.code or 500,
            "ttft": f"{(log.ttft_ms or 0) / 1000:.3f}",
            "latency": f"{(log.latency_ms or 0) / 1000:.3f}",
            "inputTokens": log.input_tokens or 0,
            "outputTokens": log.output_tokens or 0,
            "audioSeconds": log.audio_seconds or "-",
            "requestId": log.request_id or f"req_{uuid4().hex[:8]}",
            "error": log.error or "-"
        }
        for log in logs
    ]

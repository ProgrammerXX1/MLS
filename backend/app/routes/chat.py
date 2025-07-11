from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from typing import List
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
from app.config.celery_worker import celery_app
from app.services.ml import generate_response
from app.db.models import ChatLog, User
from app.core.dependencies import get_db, get_current_user
from app.schemas.chat import (
    ChatRequest, ChatLogItem, MessageResponse
)
# ✅ История сообщений

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from app.tasks import generate_response_task

router = APIRouter()

@router.post("/chat/send")
def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    
    if not request.messages or not isinstance(request.messages, list):
        raise HTTPException(status_code=400, detail="Поле 'messages' должно быть непустым списком")

    payload = {
        "messages": [msg.model_dump() for msg in request.messages],
        "model": request.model,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
        "stream": request.stream,
        "response_format": request.response_format,
        "moderation": request.moderation,
        "top_p": request.top_p,
        "seed": request.seed,
        "stop": request.stop,
        "user_id": user.id,
        "api_key": user.api_key or "",
    }

    task = generate_response_task.delay(payload)

    return JSONResponse({
        "task_id": task.id,
        "status": "submitted"
    })

@router.get("/chat/result/{task_id}")
def get_task_result(task_id: str):
    task = celery_app.AsyncResult(task_id)
    if task.state == "PENDING":
        return {"status": "processing"}
    elif task.state == "SUCCESS":
        return {
            "status": "done",
            "response_text": task.result.get("response", "⚠️ Нет ответа"),
            "input_tokens": task.result.get("input_tokens", 0),
            "output_tokens": task.result.get("output_tokens", 0),
            "latency_ms": task.result.get("latency_ms", 0),
        }
    elif task.state == "FAILURE":
        return {"status": "failed", "error": str(task.result)}


@router.get("/chat/history", response_model=List[ChatLogItem])
def get_user_chat_history(

    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    logs = (
        db.query(ChatLog)
        .filter(ChatLog.user_id == user.id)
        .order_by(ChatLog.timestamp.desc())
        .all()
    )

    return [
        ChatLogItem(
            created=log.timestamp,
            model=log.model_name or "unknown",
            api_key=log.api_key or "N/A",
            code=log.code or 200,
            ttft_ms=log.ttft_ms or 0.0,
            latency=log.latency_ms or 0.0,
            input_tokens=log.input_tokens or 0,
            output_tokens=log.output_tokens or 0,
            audio_seconds=log.audio_seconds or "-",
            request_id=log.request_id or "-",
            error=log.error or "-",
        )
        for log in logs
    ]

@router.get("/chat/result/{task_id}")
def get_task_result(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    if result.state == "PENDING":
        return {"status": "pending"}
    elif result.state == "SUCCESS":
        return {"status": "success", "response": result.result}
    elif result.state == "FAILURE":
        return {"status": "error", "error": str(result.result)}
    else:
        return {"status": result.state}

@router.get("/chat/task/{task_id}")
def get_task_result(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    if result.state == "PENDING":
        return {"status": "pending"}
    elif result.state == "SUCCESS":
        return {"status": "completed", "response": result.result}
    elif result.state == "FAILURE":
        return {"status": "failed", "error": str(result.result)}
    else:
        return {"status": result.state}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import time
import logging
from datetime import datetime
from typing import List

from services.ml import generate_response
from db.models import ChatLog, User
from core.dependencies import get_db, get_current_user
from schemas.chat import (
    ChatRequest, ChatLogItem, MessageResponse
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
router = APIRouter()

# ✅ Отправка сообщения → генерация ответа
@router.post("/chat/send", response_model=MessageResponse)
def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not request.messages or not isinstance(request.messages, list):
        raise HTTPException(status_code=400, detail="Поле 'messages' должно быть непустым списком")

    start = time.time()
    status = "success"
    error_message = ""
    model_used = request.model or "llama3:latest"

    try:
        response_text = generate_response(
            messages=[msg.model_dump() for msg in request.messages],
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=request.stream,
            response_format=request.response_format,
            moderation=request.moderation,
            top_p=request.top_p,
            seed=request.seed,
            stop=request.stop,
        )
    except Exception as e:
        logger.exception("❌ Ошибка генерации ответа от модели")
        response_text = f"Ошибка генерации: {str(e)}"
        status = "error"
        error_message = str(e)

    if not response_text.strip():
        response_text = "⚠️ Модель не смогла ответить. Попробуйте переформулировать запрос."
        status = "error"

    latency = int((time.time() - start) * 1000)

    last_user_msg = next(
        (msg.content for msg in reversed(request.messages) if msg.role == "user"), ""
    )

    # 💾 Сохраняем только лог (не создаём чат)
    log = ChatLog(
        user_id=user.id,
        api_key=user.api_key or "",
        request_text=last_user_msg,
        response_text=response_text,
        model_name=model_used,
        status=status,
        latency_ms=latency,
        timestamp=datetime.utcnow(),
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return MessageResponse(
        request_text=log.request_text,
        response_text=log.response_text,
        timestamp=log.timestamp,
        latency_ms=log.latency_ms,
    )

# ✅ История сообщений
from fastapi import Query

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
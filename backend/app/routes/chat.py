from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Union
import time
import logging

from services.ml import generate_response
from db.models import Chat, ChatLog
from core.dependencies import get_db, get_current_user
from schemas.chat import (
    ChatRequest, ChatResponse, ChatLogItem,
    ChatCreate, ChatOut, ChatUpdate, MessageResponse
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
router = APIRouter()


# ✅ Создание чата
@router.post("/chat/create", response_model=ChatOut)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_chat = Chat(
        user_id=user.id,
        title=chat.title or "Новый чат",
        status=chat.status or "Draft",
    )
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat


# ✅ Отправка сообщения (в существующий чат)
@router.post("/chat/{chat_id}/send", response_model=MessageResponse)
def send_message(chat_id: int, request: ChatRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")

    start = time.time()
    try:
        response_text = generate_response(request.message)
    except Exception as e:
        logger.exception("❌ Ошибка генерации ответа")
        raise HTTPException(status_code=500, detail="Ошибка генерации ответа")

    if not response_text.strip() or "[Empty response]" in response_text or "Ошибка" in response_text:
        response_text = "⚠️ Модель не смогла ответить. Попробуйте переформулировать запрос."

    latency = int((time.time() - start) * 1000)

    log = ChatLog(
        user_id=user.id,
        chat_id=chat_id,
        api_key=user.api_key,
        request_text=request.message,
        response_text=response_text,
        status="success",
        latency_ms=latency
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    return MessageResponse(
        request_text=log.request_text,
        response_text=log.response_text,
        timestamp=log.timestamp,
        latency_ms=log.latency_ms,
        chat_id=chat_id
    )


# ✅ Получение истории по одному чату
@router.get("/chat/{chat_id}/history", response_model=List[ChatLogItem])
def get_chat_history(chat_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")

    logs = db.query(ChatLog).filter(ChatLog.chat_id == chat_id, ChatLog.user_id == user.id).order_by(ChatLog.timestamp.desc()).all()
    return [ChatLogItem(
        request_text=l.request_text,
        response_text=l.response_text,
        timestamp=l.timestamp,
        latency_ms=l.latency_ms,
        chat_id=l.chat_id
    ) for l in logs]


# ✅ История всех чатов пользователя
@router.get("/chat/history", response_model=List[ChatLogItem])
def get_user_chat_history(db: Session = Depends(get_db), user=Depends(get_current_user)):
    logs = db.query(ChatLog).filter(ChatLog.user_id == user.id).order_by(ChatLog.timestamp.desc()).all()
    return [ChatLogItem(
        request_text=l.request_text,
        response_text=l.response_text,
        timestamp=l.timestamp,
        latency_ms=l.latency_ms,
        chat_id=l.chat_id
    ) for l in logs]


# ✅ Список всех чатов пользователя
@router.get("/chat/list", response_model=List[ChatOut])
def get_chat_list(db: Session = Depends(get_db), user=Depends(get_current_user)):
    chats = db.query(Chat).filter(Chat.user_id == user.id).order_by(Chat.created_at.desc()).all()
    return chats


# ✅ Получение одного чата
@router.get("/chat/{chat_id}", response_model=ChatOut)
def get_chat(chat_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")
    return chat


# ✅ Получение всех сообщений чата
@router.get("/chat/{chat_id}/messages", response_model=List[MessageResponse])
def get_chat_messages(chat_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")

    return [MessageResponse(
        request_text=m.request_text,
        response_text=m.response_text,
        timestamp=m.timestamp,
        latency_ms=m.latency_ms,
        chat_id=m.chat_id
    ) for m in chat.messages]


# ✅ Редактирование чата
@router.patch("/chat/{chat_id}", response_model=ChatOut)
def update_chat(chat_id: int, update: ChatUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")
    if update.title:
        chat.title = update.title
    if update.status:
        chat.status = update.status
    db.commit()
    return chat


# ✅ Удаление чата
@router.delete("/chat/{chat_id}", status_code=204)
def delete_chat(chat_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")
    db.delete(chat)
    db.commit()


# ✅ Сохранение истории сообщений
@router.post("/chat/{chat_id}/save")
def save_chat_messages(
    chat_id: int,
    messages: Union[MessageResponse, List[MessageResponse]] = Body(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")

    if isinstance(messages, MessageResponse):
        messages = [messages]

    db.query(ChatLog).filter(ChatLog.chat_id == chat_id).delete()

    for msg in messages:
        db.add(ChatLog(
            user_id=user.id,
            chat_id=chat_id,
            api_key=user.api_key,
            request_text=msg.request_text,
            response_text=msg.response_text,
            timestamp=msg.timestamp,
            latency_ms=msg.latency_ms
        ))
    db.commit()
    return {"status": "success", "count": len(messages)}

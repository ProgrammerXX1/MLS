from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Union
import time
import logging
from datetime import datetime

from services.ml import generate_response
from db.models import Chat, ChatLog, User
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

@router.post("/chat/{chat_id}/send", response_model=MessageResponse)
def send_message(
    chat_id: int,
    request: ChatRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # Проверка чата
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")

    # Проверка сообщений
    if not request.messages or not isinstance(request.messages, list):
        raise HTTPException(status_code=400, detail="Поле 'messages' должно быть непустым списком")

    start = time.time()
    status = "success"

    try:
        # Отправка сообщений в модель
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

    # Если ответ от модели пустой или странный
    if not response_text.strip() or "[Empty response]" in response_text or "Ошибка" in response_text:
        response_text = "⚠️ Модель не смогла ответить. Попробуйте переформулировать запрос."
        status = "error"

    # Метрики
    latency = int((time.time() - start) * 1000)

    # Последнее сообщение от пользователя
    last_user_msg = next(
        (msg.content for msg in reversed(request.messages) if msg.role == "user"), ""
    )

    # Логирование в базу
    log = ChatLog(
        user_id=user.id,
        api_key=user.api_key or "",
        request_text=last_user_msg,
        response_text=response_text,
        model_name=request.model,  # ✅ обязательно передаётся из запроса
        status=status,
        latency_ms=latency,
        timestamp=datetime.utcnow(),
        )
    db.add(log)
    db.commit()
    db.refresh(log)

    # Ответ клиенту
    return MessageResponse(
        request_text=log.request_text,
        response_text=log.response_text,
        timestamp=log.timestamp,
        latency_ms=log.latency_ms,
        chat_id=chat_id,
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

@router.get("/chat/single", response_model=ChatOut)
async def get_or_create_single_chat(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Пытаемся найти чат с title="single"
    chat = (
        db.query(Chat)
        .filter(Chat.user_id == user.id, Chat.title == "single")
        .first()
    )

    if chat:
        # Очищаем связанные сообщения
        db.commit()
        return chat  # ← автоматическая сериализация

    # Создаём новый "одноразовый" чат
    new_chat = Chat(user_id=user.id, title="single", status="Single")
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat  # ← тоже сериализуется в ChatOut

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



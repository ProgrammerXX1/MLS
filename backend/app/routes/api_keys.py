# routes/api_keys.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import psutil
import torch
import secrets

from core.dependencies import get_db, get_current_user
from core.API_dependencies import get_api_user, require_roles, verify_user_api_key
from db.models import User, Chat, ChatLog, APIKey, UserRole
from schemas.api_keys import APIKeyOut
from typing import List
import pynvml
from services.ml import generate_response
from schemas.chat import ChatRequest, MessageResponse

import time

pynvml.nvmlInit()

router = APIRouter()

@router.get("/api/keys/list", response_model=List[APIKeyOut])
def list_api_keys(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(APIKey).filter(APIKey.user_id == user.id).order_by(APIKey.created_at.desc()).all()

@router.post("/api/keys/create", response_model=APIKeyOut)
def create_api_key(db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_key = secrets.token_hex(32)
    api_key = APIKey(user_id=user.id, key=new_key)
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return api_key

@router.delete("/api/keys/{id}", status_code=204)
def delete_api_key(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    key = db.query(APIKey).filter(APIKey.id == id, APIKey.user_id == user.id).first()
    if not key:
        raise HTTPException(status_code=404, detail="API-ключ не найден")
    db.delete(key)
    db.commit()

@router.get("/jwt-protected")
async def jwt_protected_route(current_user: User = Depends(get_current_user)):
    print(f"✅ Проверка токена для пользователя: {current_user.username}")
    return {
        "username": current_user.username,
        "role": current_user.role  # обязательно возвращаем роль
    }

@router.get("/api-key-protected")
async def api_key_protected_route(current_user: User = Depends(get_api_user)):
    return {"username": current_user.username}



@router.get("/api/data")
async def api_data(current_user=Depends(require_roles(UserRole.admin, UserRole.coder))):
    # Логика для админа и кодера
    return {"message": "Доступ к API"}

@router.get("/chat")
async def chat_access(current_user=Depends(require_roles(UserRole.admin, UserRole.coder, UserRole.user))):
    # Логика для всех пользователей с доступом к чату
    return {"message": "Доступ к чату"}


@router.get("/admin/dashboard")
def get_admin_dashboard(db: Session = Depends(get_db), current_user=Depends(require_roles(UserRole.admin))):
    # Базовые метрики
    total_users = db.query(func.count(User.id)).scalar()
    total_chats = db.query(func.count(Chat.id)).scalar()
    total_logs = db.query(func.count(ChatLog.id)).scalar()
    total_api_keys = db.query(func.count(APIKey.id)).scalar()

    avg_latency = db.query(func.avg(ChatLog.latency_ms)).scalar() or 0
    latest_chat = db.query(Chat).order_by(Chat.created_at.desc()).first()

    # CPU и RAM
    cpu_percent = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory()
    ram_total = round(ram.total / (1024 ** 3), 2)
    ram_used = round(ram.used / (1024 ** 3), 2)

    # GPU через pynvml
    gpu_list = []
    try:
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()

        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle).decode("utf-8")
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
            temperature = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)

            gpu_list.append({
                "name": name,
                "memory_total": round(mem_info.total / (1024 ** 3), 2),
                "memory_allocated": round(mem_info.used / (1024 ** 3), 2),
                "memory_reserved": round(mem_info.total / (1024 ** 3), 2),  # Если резерв отдельно — можно заменить
                "utilization": utilization.gpu,
                "temperature": temperature
            })

        pynvml.nvmlShutdown()
    except pynvml.NVMLError as e:
        print(f"Ошибка получения GPU-информации: {str(e)}")

    # Ответ
    return {
        "users": total_users,
        "chats": total_chats,
        "logs": total_logs,
        "api_keys": total_api_keys,
        "avg_latency": round(avg_latency),
        "latest_chat_title": latest_chat.title if latest_chat else "N/A",
        "system": {
            "cpu_percent": cpu_percent,
            "ram_total": ram_total,
            "ram_used": ram_used,
            "gpus": gpu_list
        }
    }

@router.get("/admin/users_activity")
def get_users_activity(db: Session = Depends(get_db), user=Depends(require_roles(UserRole.admin))):
    # Примерная логика, адаптируй под свою схему
    return [
        {
            "id": u.id,
            "name": u.username,
            "email": u.email,
            "requests": db.query(ChatLog).filter(ChatLog.user_id == u.id).count(),
            "lastAction": db.query(ChatLog).filter(ChatLog.user_id == u.id).order_by(ChatLog.timestamp.desc()).first().timestamp
        }
        for u in db.query(User).all()
    ]


@router.post("/api/generate", response_model=MessageResponse)
def generate_with_user_key(
    request: ChatRequest,
    db: Session = Depends(get_db),
    user=Depends(verify_user_api_key)
):
    start = time.time()
    try:
        response = generate_response(request.message)
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка генерации ответа")

    latency = int((time.time() - start) * 1000)

    log = ChatLog(
        user_id=user.id,
        chat_id=None,
        api_key=user.api_key,
        request_text=request.message,
        response_text=response,
        status="success",
        latency_ms=latency
    )
    db.add(log)
    db.commit()

    return MessageResponse(
        request_text=request.message,
        response_text=response,
        timestamp=log.timestamp,
        latency_ms=latency,
        chat_id=None
    )
# routes/api_keys.py
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import func
import psutil
import secrets
from celery.result import AsyncResult
from app.config.celery_app import celery_app

import requests
from app.tasks import generate_response_task,  generate_response_api_task
from app.core.dependencies import get_db, get_current_user
from app.core.API_dependencies import get_api_user, require_roles, verify_user_api_key
from app.db.models import User, ChatLog, APIKey, UserRole
from app.schemas.api_keys import APIKeyOut
from typing import List
import pynvml
from app.services.ml import generate_response
from app.schemas.chat import ChatRequest, MessageResponse

import time
import subprocess

def init_nvml():
    try:
        pynvml.nvmlInit()
        return True
    except pynvml.NVMLError_LibraryNotFound:
        print("⚠️  NVML library not found — GPU мониторинг отключён.")
        return False
    
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

@router.get("/models")
def list_models():
    try:
        response = requests.get("http://10.121.252.227:11434/api/tags")  # для Docker
        if response.status_code == 200:
            models = response.json().get("models", [])
            return {"models": [m["name"] for m in models]}
        return {"error": f"status {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
    


@router.post("/api/generate", summary="Запуск запроса по API-ключу (через очередь)")
def generate_by_api_key(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
):
    user_id = payload.get("user_id")
    api_key_str = payload.get("api_key")

    if not user_id or not api_key_str:
        raise HTTPException(status_code=400, detail="user_id и api_key обязательны")

    # Проверка API-ключа
    api_key = db.query(APIKey).filter(APIKey.user_id == user_id, APIKey.key == api_key_str).first()
    if not api_key:
        raise HTTPException(status_code=403, detail="Неверный ключ или пользователь")

    task_payload = {
        "user_id": user_id,
        "api_key": api_key_str,
        "messages": payload.get("messages", []),
        "model": payload.get("model", "llama3"),
        "temperature": payload.get("temperature", 1.0),
        "max_tokens": payload.get("max_tokens", 1024),
        "response_format": payload.get("response_format", "text"),
        "moderation": payload.get("moderation", False),
        "top_p": payload.get("top_p", 0.75),
        "seed": payload.get("seed"),
        "stop": payload.get("stop"),
    }

    task = generate_response_api_task.delay(task_payload)
    return {"task_id": task.id}


@router.get("/api/generate/{task_id}", summary="Получить результат по task_id")
def get_response_by_task(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    if result.state == "PENDING":
        return {"status": "pending"}
    elif result.state == "FAILURE":
        return {"status": "error", "error": str(result.result)}
    elif result.state == "SUCCESS":
        return {"status": "success", "response": result.result}
    return {"status": result.state}


@router.post("/api/generate-direct", summary="Прямой вызов без очереди (нежелательно)")
def generate_with_api_key_direct(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
):
    # Такой маршрут использовать только для отладки — без очереди, всё блокирующее
    from app.services.ml import generate_response

    user_id = payload.get("user_id")
    api_key_str = payload.get("api_key")
    if not user_id or not api_key_str:
        raise HTTPException(status_code=400, detail="Missing user_id or api_key")

    key = db.query(APIKey).filter(APIKey.user_id == user_id, APIKey.key == api_key_str).first()
    if not key:
        raise HTTPException(status_code=403, detail="Invalid API key")

    try:
        result = generate_response(payload.get("messages", []))
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
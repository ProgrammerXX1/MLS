# routes/api_keys.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import psutil
import secrets

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

@router.get("/models")
def list_models():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")[1:]  # Пропускаем заголовок
        models = [line.split()[0] for line in lines]
        return {"models": models}
    except Exception as e:
        return {"error": str(e)}

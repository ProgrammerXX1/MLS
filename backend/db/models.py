from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .session import Base
from enum import Enum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_api_user = Column(Boolean, default=False)
    api_key = Column(String, unique=True, nullable=True)

    # 💬 Список API-ключей пользователя
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete")
    
    # 📜 История общения
    chat_logs = relationship("ChatLog", back_populates="user", cascade="all, delete-orphan")

    role = Column(String, default="user")  # Например: "admin", "coder", "user"


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    api_key = Column(String)
    model_name = Column(String)
    code = Column(Integer, default=200)
    ttft_ms = Column(Float, default=0.0)  # Time to first token
    latency_ms = Column(Float, default=0.0)
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    audio_seconds = Column(String, default="-")
    request_id = Column(String, default="-")
    error = Column(Text, default="-")
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_logs")


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    key = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="api_keys")

    last_used_at = Column(DateTime, nullable=True)
    usage_24h = Column(Integer, default=0)


class UserRole(str, Enum):
    admin = "admin"
    coder = "coder"
    user = "user"

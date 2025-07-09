from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .session import Base
from enum import Enum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)  # Ограничение длины
    hashed_password = Column(String, nullable=False)
    is_api_user = Column(Boolean, default=False)
    api_key = Column(String, unique=True, nullable=True)
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete")

    chats = relationship("Chat", back_populates="user", cascade="all, delete-orphan")
    chat_logs = relationship("ChatLog", back_populates="user", cascade="all, delete-orphan")

    role = Column(String, default="user")  # Ограничение длины, например, "admin", "coder", "user"

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    title = Column(String(100), default="Новый чат")  # Ограничение длины
    status = Column(String(20), nullable=False ,default="Draft")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chats")


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    api_key = Column(String, index=True)
    request_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    model_name = Column(String(100), nullable=True)  # ✅ Добавлено
    status = Column(String(20), default="success")
    latency_ms = Column(Integer)
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
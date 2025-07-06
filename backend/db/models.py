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
    messages = relationship("ChatLog", back_populates="chat", cascade="all, delete")

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=True, index=True)  # Индекс для оптимизации
    api_key = Column(String, index=True)
    request_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    status = Column(String(20), default="success")  # Ограничение длины
    latency_ms = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_logs")
    chat = relationship("Chat", back_populates="messages")

    # db/models.py
class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    key = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="api_keys")

class UserRole(str, Enum):
    admin = "admin"
    coder = "coder"
    user = "user"
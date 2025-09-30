import datetime

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String, Text

from src.database.db import Base


class ChatMessageDB(Base):
    __tablename__ = "chat_messages"

    id: int = Column(Integer, primary_key=True, index=True)
    session_id: str = Column(String, index=True)
    role: str = Column(String, index=True)
    content: str = Column(Text)
    timestamp: datetime = Column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )


class ChatSessionDB(Base):
    __tablename__ = "chat_sessions"

    id: int = Column(Integer, primary_key=True, index=True)
    session_id: str = Column(String, unique=True, index=True)
    created_at: datetime = Column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: datetime = Column(
        DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )
    message_count: int = Column(Integer, default=0)


class SessionResponse(BaseModel):
    session_id: str


class ChatRequest(BaseModel):
    message: str
    session_id: str


class ChatResponse(BaseModel):
    response: str
    session_id: str


class ChatMessage(BaseModel):
    id: int
    session_id: str
    role: str
    content: str
    timestamp: datetime.datetime

    class Config:
        from_attributes = True

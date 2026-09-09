"""Chat message schemas"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class ChatMessage(BaseModel):
    """Chat message from user or assistant"""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatMessageRequest(BaseModel):
    """Request to send a message"""
    message: str
    session_id: str | None = None


class ChatMessageResponse(BaseModel):
    """Response containing assistant message"""
    message: str
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConversationHistory(BaseModel):
    """Full conversation history"""
    session_id: str
    messages: list[ChatMessage]

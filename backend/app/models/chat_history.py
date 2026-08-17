from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime, Text
from sqlalchemy.sql import func
from app.database.base import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user_message = Column(Text, nullable=False)
    response_data = Column(JSON, nullable=False)  # Stores the full API response (outfits, context, etc.)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.sql import func
from app.database.base import Base


class FavoriteOutfit(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    outfit_data = Column(JSON, nullable=False)  # Stores the full outfit object (top, bottom, shoes, score, reasons)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.base import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    gender = Column(String)

    body_type = Column(String)

    skin_tone = Column(String)

    style_preference = Column(String)

    favorite_colors = Column(String)
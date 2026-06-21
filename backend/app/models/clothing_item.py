from sqlalchemy import Column, Integer, String
from app.database.base import Base


class ClothingItem(Base):
    __tablename__ = "clothing_items"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    category = Column(String, nullable=False)

    gender = Column(String, nullable=False)

    color = Column(String, nullable=False)

    style = Column(String, nullable=False)

    occasion = Column(String, nullable=False)

    fit = Column(String, nullable=False)

    material = Column(String, nullable=False)

    season = Column(String, nullable=False)

    tags = Column(String)

    image_url = Column(String)
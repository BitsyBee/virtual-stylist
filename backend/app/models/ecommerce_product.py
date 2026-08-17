from sqlalchemy import Column, Integer, String, Float, Text
from app.database.base import Base


class EcommerceProduct(Base):

    __tablename__ = "ecommerce_products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    brand = Column(String, nullable=False)

    source = Column(String, nullable=False)

    product_url = Column(
        String,
        nullable=False,
        unique=True
    )

    image_url = Column(String)

    price = Column(Float)

    currency = Column(
        String,
        default="LKR"
    )

    category = Column(String)

    color = Column(String)

    style = Column(String)

    availability = Column(String)

    gender = Column(String)

    occasion = Column(String)

    fit = Column(String)

    season = Column(String)

    temperature = Column(String)

    material = Column(String)

    recommended_skin_tones = Column(String)

    recommended_body_types = Column(String)

    tags = Column(String)

    description = Column(Text)

    sizes = Column(String)

    inventory_quantity = Column(Integer)
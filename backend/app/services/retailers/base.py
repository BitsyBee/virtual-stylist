from dataclasses import dataclass
from typing import Optional


@dataclass
class RetailProduct:
    name: str
    brand: str
    source: str

    product_url: str
    image_url: Optional[str] = None

    price: Optional[float] = None
    currency: str = "LKR"

    category: Optional[str] = None
    gender: Optional[str] = None
    color: Optional[str] = None
    style: Optional[str] = None

    occasion: Optional[str] = None
    fit: Optional[str] = None
    season: Optional[str] = None
    temperature: Optional[str] = None
    material: Optional[str] = None

    description: Optional[str] = None
    sizes: Optional[str] = None
    availability: Optional[str] = None

    recommended_skin_tones: Optional[str] = None
    recommended_body_types: Optional[str] = None
    tags: Optional[str] = None
from pydantic import BaseModel


class ClothingItemCreate(BaseModel):
    name: str
    category: str
    gender: str
    color: str
    style: str
    occasion: str
    fit: str
    material: str
    season: str
    recommended_skin_tones: str
    recommended_body_types: str
    temperature: str
    tags: str | None = None
    image_url: str | None = None



class ClothingItemUpdate(BaseModel):
    name: str
    category: str
    gender: str
    color: str
    style: str
    occasion: str
    fit: str
    material: str
    season: str
    recommended_skin_tones: str
    recommended_body_types: str
    temperature: str
    tags: str | None = None
    image_url: str | None = None
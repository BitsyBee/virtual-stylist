from pydantic import BaseModel


class ProfileCreate(BaseModel):
    gender: str
    body_type: str
    skin_tone: str
    style_preference: str
    favorite_colors: str
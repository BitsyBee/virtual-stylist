from pydantic import BaseModel
from datetime import datetime
from typing import Any


class FavoriteCreate(BaseModel):
    outfit_data: dict  # The complete outfit JSON


class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    outfit_data: dict
    created_at: datetime

    model_config = {"from_attributes": True}  # Pydantic V2 (replaces orm_mode)
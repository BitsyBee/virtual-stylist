from pydantic import BaseModel
from datetime import datetime


class ChatHistoryCreate(BaseModel):
    user_message: str
    response_data: dict  # The full recommendation response


class ChatHistoryResponse(BaseModel):
    id: int
    user_id: int
    user_message: str
    response_data: dict
    created_at: datetime

    model_config = {"from_attributes": True}  # Pydantic V2
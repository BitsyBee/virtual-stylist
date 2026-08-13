from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    occasion: str
    style: str
    temperature: str
    season: str
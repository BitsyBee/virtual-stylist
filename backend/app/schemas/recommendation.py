from pydantic import BaseModel


class RecommendationRequest(BaseModel):

    user_request: str
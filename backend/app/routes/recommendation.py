from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.recommendation import RecommendationRequest

from app.models.profile import Profile
from app.models.clothing_item import ClothingItem

from app.services.dependencies import get_current_user

from app.recommendation.recommendation_engine import recommend_outfits

router = APIRouter(
    prefix="/recommendation",
    tags=["Recommendation"]
)


@router.post("/")
def recommend(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    profile = db.query(Profile).filter(
        Profile.user_id == current_user["user_id"]
    ).first()

    if not profile:

        return {
            "message": "Please create your profile first."
        }

    clothing = db.query(ClothingItem).all()

    recommendations = recommend_outfits(
        profile,
        clothing,
        request.occasion,
        request.style,
        request.temperature,
        request.season 
    )

    return recommendations
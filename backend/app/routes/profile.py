from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.profile import Profile

from app.schemas.profile import ProfileCreate

from app.services.dependencies import get_current_user

router = APIRouter(prefix="/profile")


@router.post("/")
def create_profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    existing_profile = db.query(Profile).filter(
        Profile.user_id == current_user["user_id"]
    ).first()

    if existing_profile:

        return {
            "message": "Profile already exists"
        }

    new_profile = Profile(
    user_id=current_user["user_id"],
    gender=profile.gender,
    body_type=profile.body_type,
    skin_tone=profile.skin_tone,
    style_preference=profile.style_preference,
    favorite_colors=profile.favorite_colors
)

    db.add(new_profile)

    db.commit()

    return {
        "message": "Profile created successfully"
    }


@router.get("/")
def get_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    profile = db.query(Profile).filter(
        Profile.user_id == current_user["user_id"]
    ).first()

    return profile
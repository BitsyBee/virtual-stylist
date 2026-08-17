from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate
from app.services.dependencies import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("/")
def create_profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    existing = db.query(Profile).filter(
        Profile.user_id == current_user["user_id"]
    ).first()

    if existing:
        return {"message": "Profile already exists"}

    new_profile = Profile(
        user_id=current_user["user_id"],
        gender=profile.gender,
        body_type=profile.body_type,
        skin_tone=profile.skin_tone,
        style_preference=profile.style_preference,
        favorite_colors=profile.favorite_colors,
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return {"message": "Profile created successfully"}


@router.get("/")
def get_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    profile = db.query(Profile).filter(
        Profile.user_id == current_user["user_id"]
    ).first()
    return profile


@router.put("/")
def upsert_profile(
    profile_data: ProfileCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # 🔥 FIX: Try to find existing profile
    profile = db.query(Profile).filter(
        Profile.user_id == current_user["user_id"]
    ).first()

    if not profile:
        # 🟢 CREATE new profile if it doesn't exist
        new_profile = Profile(
            user_id=current_user["user_id"],
            gender=profile_data.gender,
            body_type=profile_data.body_type,
            skin_tone=profile_data.skin_tone,
            style_preference=profile_data.style_preference,
            favorite_colors=profile_data.favorite_colors,
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return {"message": "Profile created successfully", "action": "created"}

    # 🟡 UPDATE existing profile
    profile.gender = profile_data.gender
    profile.body_type = profile_data.body_type
    profile.skin_tone = profile_data.skin_tone
    profile.style_preference = profile_data.style_preference
    profile.favorite_colors = profile_data.favorite_colors
    db.commit()
    db.refresh(profile)

    return {"message": "Profile updated successfully", "action": "updated"}
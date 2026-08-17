from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models.favorite import FavoriteOutfit
from app.schemas.favorite import FavoriteCreate, FavoriteResponse
from app.services.dependencies import get_current_user

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.post("/", response_model=FavoriteResponse)
def save_favorite(
    favorite: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_favorite = FavoriteOutfit(
        user_id=current_user["user_id"],
        outfit_data=favorite.outfit_data,
    )
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite


@router.get("/", response_model=List[FavoriteResponse])
def list_favorites(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return (
        db.query(FavoriteOutfit)
        .filter(FavoriteOutfit.user_id == current_user["user_id"])
        .order_by(FavoriteOutfit.created_at.desc())
        .all()
    )


@router.delete("/{favorite_id}")
def delete_favorite(
    favorite_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    favorite = (
        db.query(FavoriteOutfit)
        .filter(
            FavoriteOutfit.id == favorite_id,
            FavoriteOutfit.user_id == current_user["user_id"],
        )
        .first()
    )
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    db.delete(favorite)
    db.commit()
    return {"message": "Favorite removed"}
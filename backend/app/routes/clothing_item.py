from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.clothing_item import ClothingItem
from app.schemas.clothing_item import (
    ClothingItemCreate,
    ClothingItemUpdate
)

router = APIRouter(
    prefix="/clothing-items",
    tags=["Clothing Items"]
)


@router.post("/")
def create_clothing_item(
    item: ClothingItemCreate,
    db: Session = Depends(get_db)
):

    clothing = ClothingItem(
        name=item.name,
        category=item.category,
        gender=item.gender,
        color=item.color,
        style=item.style,
        occasion=item.occasion,
        fit=item.fit,
        material = item.material,
        season=item.season,
        recommended_skin_tones=item.recommended_skin_tones,
        recommended_body_types=item.recommended_body_types,
        temperature=item.temperature,
        tags=item.tags,
        image_url=item.image_url
    )

    db.add(clothing)
    db.commit()
    db.refresh(clothing)

    return {
        "message": "Clothing item created successfully",
        "id": clothing.id
    }


@router.get("/")
def get_all_clothing_items(
    db: Session = Depends(get_db)
):

    return db.query(ClothingItem).all()


@router.get("/{item_id}")
def get_clothing_item(
    item_id: int,
    db: Session = Depends(get_db)
):

    return db.query(ClothingItem).filter(
        ClothingItem.id == item_id
    ).first()


@router.put("/{item_id}")
def update_clothing_item(
    item_id: int,
    item: ClothingItemUpdate,
    db: Session = Depends(get_db)
):

    clothing = db.query(ClothingItem).filter(
        ClothingItem.id == item_id
    ).first()

    if not clothing:
        return {"message": "Item not found"}

    clothing.name = item.name
    clothing.category = item.category
    clothing.gender = item.gender
    clothing.color = item.color
    clothing.style = item.style
    clothing.occasion = item.occasion
    clothing.fit = item.fit
    clothing.material = item.material 
    clothing.season = item.season
    clothing.recommended_skin_tones = item.recommended_skin_tones
    clothing.recommended_body_types = item.recommended_body_types
    clothing.temperature = item.temperature
    clothing.tags = item.tags
    clothing.image_url = item.image_url

    db.commit()

    return {
        "message": "Item updated successfully"
    }


@router.delete("/{item_id}")
def delete_clothing_item(
    item_id: int,
    db: Session = Depends(get_db)
):

    clothing = db.query(ClothingItem).filter(
        ClothingItem.id == item_id
    ).first()

    if not clothing:
        return {"message": "Item not found"}

    db.delete(clothing)
    db.commit()

    return {
        "message": "Item deleted successfully"
    }
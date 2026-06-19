from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth import hash_password
from app.schemas.auth import LoginRequest
from app.services.auth import verify_password
from app.services.jwt_handler import create_access_token

router = APIRouter()


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {
        "message": "User created successfully",
        "user_id": db_user.id
    }

@router.post("/login")
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == credentials.email
    ).first()

    if not user:
        return {
            "message": "Invalid credentials"
        }

    if not verify_password(
        credentials.password,
        user.password_hash
    ):
        return {
            "message": "Invalid credentials"
        }

    token = create_access_token(
        {
            "user_id": user.id,
            "email": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models.chat_history import ChatHistory
from app.schemas.chat_history import ChatHistoryCreate, ChatHistoryResponse
from app.services.dependencies import get_current_user

router = APIRouter(prefix="/chat/history", tags=["Chat History"])


@router.post("/", response_model=ChatHistoryResponse)
def save_chat_entry(
    entry: ChatHistoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_entry = ChatHistory(
        user_id=current_user["user_id"],
        user_message=entry.user_message,
        response_data=entry.response_data,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@router.get("/", response_model=List[ChatHistoryResponse])
def list_chat_history(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == current_user["user_id"])
        .order_by(ChatHistory.created_at.desc())
        .limit(limit)
        .all()
    )
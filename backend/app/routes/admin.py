from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.services.admin_service import (
    admin_login,
    create_question,
    update_question,
    delete_question
)

from backend.app.schemas.admin import (
    AdminLoginRequest,
    QuestionCreateRequest,
    QuestionUpdateRequest
)

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/login")
def login(request: AdminLoginRequest, db: Session = Depends(get_db)):
    return admin_login(db, request)


@router.post("/questions")
def create(request: QuestionCreateRequest, db: Session = Depends(get_db)):
    return create_question(db, request)


@router.put("/questions/{question_id}")
def update(question_id: int, request: QuestionUpdateRequest, db: Session = Depends(get_db)):
    return update_question(db, question_id, request)


@router.delete("/questions/{question_id}")
def delete(question_id: int, db: Session = Depends(get_db)):
    return delete_question(db, question_id)
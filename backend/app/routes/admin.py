from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..dependencies.admin import get_current_admin
from ..services.admin_service import (
    admin_login,
    create_question,
    update_question,
    delete_question,
    get_all_questions
)

from ..schemas.admin import (
    AdminLoginRequest,
    QuestionCreateRequest,
    QuestionUpdateRequest
)

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/login")
def login(request: AdminLoginRequest, db: Session = Depends(get_db)):
    return admin_login(db, request)


@router.get("/questions")
def get_questions(
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return get_all_questions(db)


@router.post("/questions")
def create(
    request: QuestionCreateRequest,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return create_question(db, request)


@router.put("/questions/{question_id}")
def update(
    question_id: int,
    request: QuestionUpdateRequest,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return update_question(db, question_id, request)


@router.delete("/questions/{question_id}")
def delete(
    question_id: int,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return delete_question(db, question_id)
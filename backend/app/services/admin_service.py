from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models.admin_user import AdminUser
from ..models.question import Question

from ..schemas.admin import (
    AdminLoginRequest,
    QuestionCreateRequest,
    QuestionUpdateRequest
)

from ..utils.security.password import verify_password, hash_password
from ..utils.security.token import generate_token


# ---------------- AUTH ----------------

def admin_login(db: Session, request: AdminLoginRequest):

    admin = db.query(AdminUser).filter(
        AdminUser.username == request.username
    ).first()

    if not admin or not admin.is_active:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(request.password, admin.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = generate_token(admin)

    admin.token = token
    db.commit()

    return {
        "message": "Login successful",
        "token": token
    }


# ---------------- QUESTIONS ----------------

def create_question(db: Session, request: QuestionCreateRequest):

    question = Question(**request.dict())

    db.add(question)
    db.commit()
    db.refresh(question)

    return question


def update_question(db: Session, question_id: int, request: QuestionUpdateRequest):

    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    for k, v in request.dict(exclude_unset=True).items():
        setattr(question, k, v)

    db.commit()
    db.refresh(question)

    return question


def delete_question(db: Session, question_id: int):

    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(question)
    db.commit()

    return {"message": "deleted"}


def get_all_questions(db: Session):

    return db.query(Question).order_by(Question.id.desc()).all()
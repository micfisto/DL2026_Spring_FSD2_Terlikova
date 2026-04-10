from sqlalchemy.orm import Session
from fastapi import HTTPException

from backend.app.models.admin_user import AdminUser
from backend.app.models.question import Question

from backend.app.schemas.admin import (
    AdminLoginRequest,
    QuestionCreateRequest,
    QuestionUpdateRequest
)
from backend.app.utils.security import (hash_password, verify_password)


def admin_login(db: Session, request: AdminLoginRequest):
    admin = db.query(AdminUser).filter(
        AdminUser.username == request.username
    ).first()

    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(request.password, admin.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "admin_id": admin.id
    }

def create_admin(db: Session, username: str, email: str, password: str):
    admin = AdminUser(
        username=username,
        email=email,
        password=hash_password(password),
        is_active=True
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return admin

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

    for key, value in request.dict(exclude_unset=True).items():
        setattr(question, key, value)

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

from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models.admin_user import AdminUser
from ..models.question import Question

from ..schemas.admin import (
    AdminLoginRequest,
    QuestionCreateRequest,
    QuestionUpdateRequest
)

from ..utils.security.password import verify_password
from ..utils.security.token import generate_token


# ---------------- VALIDATION ----------------

def validate_country_code(v):
    if v is None:
        raise HTTPException(status_code=422, detail="country_code is required")

    v = str(v).strip().upper()

    if len(v) != 3 or not v.isalpha():
        raise HTTPException(status_code=422, detail="country_code must be 3 letters")

    return v


def validate_required_text(v, field_name: str):
    if v is None:
        raise HTTPException(status_code=422, detail=f"{field_name} is required")

    v = str(v).strip()

    if v == "":
        raise HTTPException(status_code=422, detail=f"{field_name} cannot be empty")

    return v


def validate_lat_lng(lat, lng):
    if lat is None or lng is None:
        raise HTTPException(status_code=422, detail="lat/lng are required")

    try:
        lat = float(lat)
        lng = float(lng)
    except:
        raise HTTPException(status_code=422, detail="lat/lng must be numbers")

    if not (-90 <= lat <= 90):
        raise HTTPException(status_code=422, detail="lat out of range")

    if not (-180 <= lng <= 180):
        raise HTTPException(status_code=422, detail="lng out of range")

    return lat, lng


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

    data = request.dict()

    data["question_text"] = validate_required_text(data.get("question_text"), "question_text")
    data["target_name"] = validate_required_text(data.get("target_name"), "target_name")

    data["country_code"] = validate_country_code(data.get("country_code"))

    lat, lng = validate_lat_lng(data.get("correct_lat"), data.get("correct_lng"))
    data["correct_lat"] = lat
    data["correct_lng"] = lng

    question = Question(**data)

    db.add(question)
    db.commit()
    db.refresh(question)

    return question


def update_question(db: Session, question_id: int, request: QuestionUpdateRequest):

    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    data = request.dict(exclude_unset=True)

    for k, v in data.items():

        if k == "question_text":
            v = validate_required_text(v, "question_text")

        if k == "target_name":
            v = validate_required_text(v, "target_name")

        if k == "country_code":
            v = validate_country_code(v)

        if k in ["correct_lat", "correct_lng"]:
            lat = data.get("correct_lat", question.correct_lat)
            lng = data.get("correct_lng", question.correct_lng)

            lat, lng = validate_lat_lng(lat, lng)

            question.correct_lat = lat
            question.correct_lng = lng
            continue

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
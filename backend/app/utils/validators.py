from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.app.models.session_question import SessionQuestion
from backend.app.models.answer import Answer


# Проверяет, что вопрос принадлежит указанной игровой сессии.
def validate_question_belongs_to_session(
        db: Session,
        session_id: int,
        question_id: int
) -> SessionQuestion:
    session_question = db.query(SessionQuestion).filter(
        SessionQuestion.session_id == session_id,
        SessionQuestion.question_id == question_id
    ).first()

    if not session_question:
        raise HTTPException(
            status_code=400,
            detail="Вопрос не принадлежит этой игровой сессии"
        )

    return session_question


# Проверяет, был ли уже дан ответ на вопрос в сессии.
def check_answer_already_exists(
        db: Session,
        session_id: int,
        question_id: int
) -> bool:
    return db.query(Answer).filter(
        Answer.session_id == session_id,
        Answer.question_id == question_id
    ).first() is not None

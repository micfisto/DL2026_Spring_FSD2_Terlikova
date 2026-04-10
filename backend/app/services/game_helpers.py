from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.app.models.question import Question
from backend.app.models.session_question import SessionQuestion
from backend.app.models.game_session import GameSession

#    Получает сессию игры или выбрасывает 404
def get_session_or_404(db: Session, session_id: int) -> GameSession:
    session = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    return session

# Проверяет, что сессия активна
def check_session_active(session: GameSession) -> None:
    if session.status != "active":
        raise HTTPException(status_code=400, detail="Игра уже завершена")

# Получает текущий вопрос сессии по индексу
def get_current_session_question(db: Session, session: GameSession) -> Question:
    session_question = db.query(SessionQuestion).filter(
        SessionQuestion.session_id == session.id,
        SessionQuestion.order_index == session.current_question_index
    ).first()
    
    if not session_question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    question = db.query(Question).filter(Question.id == session_question.question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    return question

# Получает вопрос по ID
def get_question_by_id(db: Session, question_id: int) -> Question:
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    return question

# Получает вопрос по порядковому индексу в сессии
def get_question_by_order_index(db: Session, session: GameSession, order_index: int) -> Question:
    sq = db.query(SessionQuestion).filter(
        SessionQuestion.session_id == session.id,
        SessionQuestion.order_index == order_index
    ).first()
    
    if not sq:
        return None
    
    return db.query(Question).filter(Question.id == sq.question_id).first()

# Проверяет, является ли текущий вопрос последним
def is_last_question(session: GameSession) -> bool:
    return session.current_question_index + 1 >= session.total_questions
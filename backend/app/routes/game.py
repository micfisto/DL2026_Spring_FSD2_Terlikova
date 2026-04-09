import math
import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.db import get_db
from backend.app.models.question import Question
from backend.app.models.answer import Answer
from backend.app.models.game_session import GameSession
from backend.app.models.session_question import SessionQuestion

from backend.app.schemas.game import (
    StartGameRequest,
    StartGameResponse,
    QuestionResponse,
    ProgressResponse,
    NextQuestionResponse,
    SubmitAnswerResponse,
    SubmitAnswerRequest,
    GameFinishedResponse,
    FinishGameResponse,
    GameResultResponse
)

router = APIRouter(prefix="/api/game", tags=["Game"])

@router.get("/test")
def test_game():
    return {"message": "Game router works"}

def calculate_distance_km(lat1, lng1, lat2, lng2):
    R = 6371

    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)

    a = (
            math.sin(d_lat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(d_lng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(R * c, 2)


def calculate_points(distance_km: float) -> int:
    points = max(0, 1000 - int(distance_km * 10))
    return points


@router.post("/start", response_model=StartGameResponse)
def start_game(request: StartGameRequest, db: Session = Depends(get_db)):
    questions = (
        db.query(Question)
        .filter(
            Question.mode == request.mode,
            Question.difficulty == request.difficulty,
            Question.is_active == True
        )
        .order_by(func.random())
        .limit(request.question_count)
        .all()
    )

    if len(questions) < request.question_count:
        raise HTTPException(
            status_code=400,
            detail="Недостаточно вопросов для выбранного режима и сложности"
        )

    session = GameSession(
        mode=request.mode,
        difficulty=request.difficulty,
        total_questions=request.question_count,
        current_question_index=0,
        score=0,
        status="active"
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    for index, question in enumerate(questions):
        session_question = SessionQuestion(
            session_id=session.id,
            question_id=question.id,
            order_index=index
        )
        db.add(session_question)

    db.commit()

    first_question = questions[0]

    return StartGameResponse(
        session_id=session.id,
        question=QuestionResponse(
            question_id=first_question.id,
            text=first_question.question_text,
            target_type=first_question.target_type
        ),
        progress=ProgressResponse(current=1, total=session.total_questions),
        score=session.score
    )

@router.get("/{session_id}/question", response_model=NextQuestionResponse)
def get_current_question(session_id: int, db: Session = Depends(get_db)):
    session = db.query(GameSession).filter(GameSession.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")

    if session.status != "active":
        raise HTTPException(status_code=400, detail="Игра уже завершена")

    session_question = (
        db.query(SessionQuestion)
        .filter(
            SessionQuestion.session_id == session.id,
            SessionQuestion.order_index == session.current_question_index
        )
        .first()
    )

    if not session_question:
        raise HTTPException(status_code=404, detail="Текущий вопрос не найден")

    question = db.query(Question).filter(Question.id == session_question.question_id).first()

    return NextQuestionResponse(
        question=QuestionResponse(
            question_id=question.id,
            text=question.question_text,
            target_type=question.target_type
        ),
        progress=ProgressResponse(
            current=session.current_question_index + 1,
            total=session.total_questions
        ),
        score=session.score
    )

@router.post("/{session_id}/answer", response_model=SubmitAnswerResponse)
def submit_answer(session_id: int, request: SubmitAnswerRequest, db: Session = Depends(get_db)):
    session = db.query(GameSession).filter(GameSession.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")

    if session.status != "active":
        raise HTTPException(status_code=400, detail="Игра уже завершена")

    existing_answer = (
        db.query(Answer)
        .filter(
            Answer.session_id == session_id,
            Answer.question_id == request.question_id
        )
        .first()
    )

    if existing_answer:
        raise HTTPException(status_code=400, detail="Ответ на этот вопрос уже отправлен")

    question = db.query(Question).filter(Question.id == request.question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    distance_km = calculate_distance_km(
        request.selected_lat,
        request.selected_lng,
        question.correct_lat,
        question.correct_lng
    )

    points = calculate_points(distance_km)

    answer = Answer(
        session_id=session.id,
        question_id=question.id,
        selected_lat=request.selected_lat,
        selected_lng=request.selected_lng,
        distance_km=distance_km,
        points_earned=points,
        answered_at=datetime.datetime.utcnow()
    )

    db.add(answer)

    session.score += points

    is_last_question = session.current_question_index + 1 >= session.total_questions

    db.commit()

    return SubmitAnswerResponse(
        question_id=question.id,
        correct_lat=question.correct_lat,
        correct_lng=question.correct_lng,
        distance_km=distance_km,
        points_earned=points,
        total_score=session.score,
        is_last_question=is_last_question
    )

@router.get("/{session_id}/next", response_model=NextQuestionResponse | GameFinishedResponse)
def get_next_question(session_id: int, db: Session = Depends(get_db)):
    session = db.query(GameSession).filter(GameSession.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")

    if session.status != "active":
        raise HTTPException(status_code=400, detail="Игра уже завершена")

    current_session_question = (
        db.query(SessionQuestion)
        .filter(
            SessionQuestion.session_id == session.id,
            SessionQuestion.order_index == session.current_question_index
        )
        .first()
    )

    if not current_session_question:
        raise HTTPException(status_code=404, detail="Текущий вопрос не найден")

    current_answer = (
        db.query(Answer)
        .filter(
            Answer.session_id == session.id,
            Answer.question_id == current_session_question.question_id
        )
        .first()
    )

    if not current_answer:
        raise HTTPException(status_code=400, detail="Сначала нужно ответить на текущий вопрос")

    session.current_question_index += 1

    if session.current_question_index >= session.total_questions:
        session.status = "finished"
        session.finished_at = datetime.datetime.utcnow()
        db.commit()

        return GameFinishedResponse(
            final_score=session.score
        )

    next_session_question = (
        db.query(SessionQuestion)
        .filter(
            SessionQuestion.session_id == session.id,
            SessionQuestion.order_index == session.current_question_index
        )
        .first()
    )

    question = db.query(Question).filter(Question.id == next_session_question.question_id).first()

    db.commit()

    return NextQuestionResponse(
        question=QuestionResponse(
            question_id=question.id,
            text=question.question_text,
            target_type=question.target_type
        ),
        progress=ProgressResponse(
            current=session.current_question_index + 1,
            total=session.total_questions
        ),
        score=session.score
    )

@router.post("/{session_id}/finish", response_model=FinishGameResponse)
def finish_game(session_id: int, db: Session = Depends(get_db)):
    session = db.query(GameSession).filter(GameSession.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")

    if session.status == "finished":
        raise HTTPException(status_code=400, detail="Сессия уже завершена")

    session.status = "finished"
    session.finished_at = datetime.datetime.utcnow()

    answered_questions = db.query(Answer).filter(Answer.session_id == session.id).count()

    db.commit()

    return FinishGameResponse(
        session_id=session.id,
        status=session.status,
        answered_questions=answered_questions,
        total_questions=session.total_questions,
        final_score=session.score
    )

@router.get("/{session_id}/result", response_model=GameResultResponse)
def get_game_result(session_id: int, db: Session = Depends(get_db)):
    session = db.query(GameSession).filter(GameSession.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")

    if session.status != "finished":
        raise HTTPException(status_code=400, detail="Игра ещё не завершена")

    answered_questions = db.query(Answer).filter(Answer.session_id == session.id).count()

    return GameResultResponse(
        session_id=session.id,
        mode=session.mode,
        final_score=session.score,
        answered_questions=answered_questions,
        total_questions=session.total_questions,
        finished_at=session.finished_at
    )
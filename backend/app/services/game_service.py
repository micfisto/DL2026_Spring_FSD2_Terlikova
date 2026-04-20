import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.question import Question
from ..models.answer import Answer
from ..models.game_session import GameSession
from ..models.session_question import SessionQuestion

from ..schemas.game import (
    StartGameRequest,
    StartGameResponse,
    QuestionResponse,
    ProgressResponse,
    NextQuestionResponse,
    SubmitAnswerResponse,
    GameFinishedResponse,
    FinishGameResponse,
    GameResultResponse,
    SubmitAnswerRequest
)

from ..utils.math.distance import calculate_distance_km
from ..utils.math.scoring import calculate_points, get_max_points_for_difficulty
from ..utils.geo.country import point_in_country


# ---------------- helpers ----------------

def _session(db: Session, session_id: int):
    session = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    return session


def _answered_count(db: Session, session_id: int):
    return db.query(Answer).filter(Answer.session_id == session_id).count()


def _question(db: Session, session_id: int, index: int):
    sq = db.query(SessionQuestion).filter(
        SessionQuestion.session_id == session_id,
        SessionQuestion.order_index == index
    ).first()

    if not sq:
        return None

    return db.query(Question).filter(Question.id == sq.question_id).first()


def _format(q: Question) -> QuestionResponse:
    return QuestionResponse(
        question_id=q.id,
        text=q.question_text,
        target_type=q.target_type,
        target_name=q.target_name,
        correct_country_code=q.target_name if q.target_type == "country" else None
    )


def _is_last(db: Session, session: GameSession):
    return _answered_count(db, session.id) >= session.total_questions


# ---------------- core ----------------

def start_game(db: Session, request: StartGameRequest):

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

    if not questions:
        raise HTTPException(status_code=400, detail="Нет вопросов")

    session = GameSession(
        mode=request.mode,
        difficulty=request.difficulty,
        total_questions=len(questions),
        score=0,
        status="active",
        started_at=datetime.datetime.utcnow()
    )

    db.add(session)
    db.flush()

    for i, q in enumerate(questions):
        db.add(SessionQuestion(
            session_id=session.id,
            question_id=q.id,
            order_index=i
        ))

    db.commit()

    first = _question(db, session.id, 0)

    return StartGameResponse(
        session_id=session.id,
        question=_format(first),
        progress=ProgressResponse(current=1, total=len(questions)),
        score=0
    )


def get_current_question(db: Session, session_id: int):

    session = _session(db, session_id)

    index = _answered_count(db, session_id)
    q = _question(db, session_id, index)

    if not q:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    return NextQuestionResponse(
        question=_format(q),
        progress=ProgressResponse(current=index + 1, total=session.total_questions),
        score=session.score
    )


def submit_answer(db: Session, session_id: int, request: SubmitAnswerRequest):

    session = _session(db, session_id)

    index = _answered_count(db, session_id)
    q = _question(db, session_id, index)

    if not q or q.id != request.question_id:
        raise HTTPException(status_code=400, detail="Неверный вопрос")

    distance = None
    points = 0

    if q.target_type == "country":

        ok = point_in_country(
            request.selected_lat,
            request.selected_lng,
            q.target_name
        )

        if ok:
            points = get_max_points_for_difficulty(session.difficulty)
            distance = 0
        else:
            distance = calculate_distance_km(
                request.selected_lat,
                request.selected_lng,
                q.correct_lat,
                q.correct_lng
            )
            points = calculate_points(distance, session.difficulty)

    else:
        distance = calculate_distance_km(
            request.selected_lat,
            request.selected_lng,
            q.correct_lat,
            q.correct_lng
        )
        points = calculate_points(distance, session.difficulty)

    db.add(Answer(
        session_id=session.id,
        question_id=q.id,
        selected_lat=request.selected_lat,
        selected_lng=request.selected_lng,
        distance_km=distance,
        points_earned=points,
        answered_at=datetime.datetime.utcnow()
    ))

    session.score += points
    db.commit()

    return SubmitAnswerResponse(
        question_id=q.id,
        correct_lat=q.correct_lat,
        correct_lng=q.correct_lng,
        distance_km=distance,
        points_earned=points,
        total_score=session.score,
        is_last_question=_is_last(db, session)
    )


def get_next_question(db: Session, session_id: int):

    session = _session(db, session_id)

    next_index = _answered_count(db, session_id)

    if next_index >= session.total_questions:
        session.status = "finished"
        session.finished_at = datetime.datetime.utcnow()
        db.commit()

        return GameFinishedResponse(final_score=session.score)

    q = _question(db, session_id, next_index)

    db.commit()

    return NextQuestionResponse(
        question=_format(q),
        progress=ProgressResponse(current=next_index + 1, total=session.total_questions),
        score=session.score
    )


def finish_game(db: Session, session_id: int):

    session = _session(db, session_id)

    session.status = "finished"
    session.finished_at = datetime.datetime.utcnow()

    db.commit()

    return FinishGameResponse(
        session_id=session.id,
        status=session.status,
        answered_questions=_answered_count(db, session_id),
        total_questions=session.total_questions,
        final_score=session.score
    )


def get_game_result(db: Session, session_id: int):

    session = _session(db, session_id)

    if session.status != "finished":
        raise HTTPException(status_code=400, detail="Игра не завершена")

    return GameResultResponse(
        session_id=session.id,
        mode=session.mode,
        final_score=session.score,
        answered_questions=_answered_count(db, session_id),
        total_questions=session.total_questions,
        finished_at=session.finished_at
    )
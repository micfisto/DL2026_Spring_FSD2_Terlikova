import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

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
    GameFinishedResponse,
    FinishGameResponse,
    GameResultResponse,
    SubmitAnswerRequest
)

from backend.app.utils.calculate_distance import calculate_distance_km
from backend.app.utils.calculate_points import calculate_points

from backend.app.utils.validators import (
    validate_question_belongs_to_session,
    check_answer_already_exists
)
from backend.app.services.game_helpers import (
    get_session_or_404,
    check_session_active,
    get_current_session_question,
    get_question_by_id,
    get_question_by_order_index,
    is_last_question
)


# Начать новую игровую сессию
def start_game(db: Session, request: StartGameRequest) -> StartGameResponse:
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
        raise HTTPException(status_code=400, detail="Недостаточно вопросов")

    session = GameSession(
        mode=request.mode,
        difficulty=request.difficulty,
        total_questions=request.question_count,
        current_question_index=0,
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

    first_question = questions[0]

    return StartGameResponse(
        session_id=session.id,
        question=QuestionResponse(
            question_id=first_question.id,
            text=first_question.question_text,
            target_type=first_question.target_type
        ),
        progress=ProgressResponse(
            current=1,
            total=session.total_questions),
        score=session.score
    )


# Получить текущий вопрос игры
def get_current_question(db: Session, session_id: int) -> NextQuestionResponse:
    session = get_session_or_404(db, session_id)
    check_session_active(session)

    question = get_current_session_question(db, session)

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


# Отправить ответ на вопрос
def submit_answer(db: Session, session_id: int, request: SubmitAnswerRequest):
    session = get_session_or_404(db, session_id)
    check_session_active(session)

    validate_question_belongs_to_session(db, session_id, request.question_id)

    if check_answer_already_exists(db, session_id, request.question_id):
        raise HTTPException(status_code=400, detail="Уже отвечали")

    question = get_question_by_order_index(db, session, session.current_question_index)

    if not question or question.id != request.question_id:
        raise HTTPException(status_code=400, detail="Нельзя отвечать не на текущий вопрос")

    distance = calculate_distance_km(
        request.selected_lat,
        request.selected_lng,
        question.correct_lat,
        question.correct_lng
    )

    points = calculate_points(distance)

    answer = Answer(
        session_id=session.id,
        question_id=question.id,
        selected_lat=request.selected_lat,
        selected_lng=request.selected_lng,
        distance_km=distance,
        points_earned=points,
        answered_at=datetime.datetime.utcnow()
    )

    db.add(answer)
    session.score += points

    is_last = is_last_question(session)

    db.commit()

    return SubmitAnswerResponse(
        question_id=question.id,
        correct_lat=question.correct_lat,
        correct_lng=question.correct_lng,
        distance_km=distance,
        points_earned=points,
        total_score=session.score,
        is_last_question=is_last
    )


# Перейти к следующему вопросу
def get_next_question(db: Session, session_id: int):
    session = get_session_or_404(db, session_id)
    check_session_active(session)

    session.current_question_index += 1

    if session.current_question_index >= session.total_questions:
        session.status = "finished"
        session.finished_at = datetime.datetime.utcnow()
        db.commit()

        return GameFinishedResponse(final_score=session.score)

    question = get_question_by_order_index(db, session, session.current_question_index)

    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

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


# Досрочно завершить игру
def finish_game(db: Session, session_id: int):
    session = get_session_or_404(db, session_id)

    session.status = "finished"
    session.finished_at = datetime.datetime.utcnow()

    answered = db.query(Answer).filter(Answer.session_id == session.id).count()

    db.commit()

    return FinishGameResponse(
        session_id=session.id,
        status=session.status,
        answered_questions=answered,
        total_questions=session.total_questions,
        final_score=session.score
    )


# Получить результаты завершённой игры
def get_game_result(db: Session, session_id: int):
    session = get_session_or_404(db, session_id)

    if session.status != "finished":
        raise HTTPException(status_code=400, detail="Игра не завершена")

    answered = db.query(Answer).filter(Answer.session_id == session.id).count()

    return GameResultResponse(
        session_id=session.id,
        mode=session.mode,
        final_score=session.score,
        answered_questions=answered,
        total_questions=session.total_questions,
        finished_at=session.finished_at
    )

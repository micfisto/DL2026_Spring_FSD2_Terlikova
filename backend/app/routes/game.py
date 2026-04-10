from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.services import game_service
from backend.app.schemas.game import (
    StartGameRequest,
    StartGameResponse,
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


@router.post("/start", response_model=StartGameResponse)
def start_game(request: StartGameRequest, db: Session = Depends(get_db)):
    return game_service.start_game(db, request)


@router.get("/{session_id}/question", response_model=NextQuestionResponse)
def get_current_question(session_id: int, db: Session = Depends(get_db)):
    return game_service.get_current_question(db, session_id)


@router.post("/{session_id}/answer", response_model=SubmitAnswerResponse)
def submit_answer(session_id: int, request: SubmitAnswerRequest, db: Session = Depends(get_db)):
    return game_service.submit_answer(db, session_id, request)


@router.get("/{session_id}/next", response_model=NextQuestionResponse | GameFinishedResponse)
def get_next_question(session_id: int, db: Session = Depends(get_db)):
    return game_service.get_next_question(db, session_id)

@router.post("/{session_id}/finish", response_model=FinishGameResponse)
def finish_game(session_id: int, db: Session = Depends(get_db)):
    return game_service.finish_game(db, session_id)


@router.get("/{session_id}/result", response_model=GameResultResponse)
def get_game_result(session_id: int, db: Session = Depends(get_db)):
    return game_service.get_game_result(db, session_id)
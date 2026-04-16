from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..services.leaderboard_service import (
    save_leaderboard,
    get_leaderboard,
    get_leaderboard_with_user
)
from ..schemas.leaderboard import SaveLeaderboardRequest

router = APIRouter(prefix="/api/leaderboard", tags=["Leaderboard"])


@router.post("/save")
def save(request: SaveLeaderboardRequest, db: Session = Depends(get_db)):
    try:
        return save_leaderboard(db, request.session_id, request.player_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def list_leaderboard(
    mode: str,
    db: Session = Depends(get_db)
):
    return get_leaderboard(db, mode)


@router.get("/with-user")
def get_leaderboard_user(
    mode: str,
    user_entry_id: int = Query(None),
    db: Session = Depends(get_db)
):
    return get_leaderboard_with_user(db, mode, user_entry_id)
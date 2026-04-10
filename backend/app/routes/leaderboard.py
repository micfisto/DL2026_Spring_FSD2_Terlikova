from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.services.leaderboard_service import (
    save_leaderboard,
    get_leaderboard
)
from backend.app.schemas.leaderboard import SaveLeaderboardRequest

router = APIRouter(prefix="/api/leaderboard", tags=["Leaderboard"])


@router.post("/save")
def save(request: SaveLeaderboardRequest, db: Session = Depends(get_db)):
    try:
        return save_leaderboard(db, request.session_id, request.player_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/")
def list_leaderboard(mode: str, db: Session = Depends(get_db)):
    try:
        return get_leaderboard(db, mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
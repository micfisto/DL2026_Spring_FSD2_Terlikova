import datetime
from datetime import datetime as dt
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.models.leaderboard_entry import LeaderboardEntry
from backend.app.models.game_session import GameSession

from backend.app.schemas.leaderboard import (
    SaveLeaderboardResponse,
    LeaderboardItem,
    LeaderboardResponse
)

def save_leaderboard(db: Session, session_id: int, player_name: str):

    session = db.query(GameSession).filter(GameSession.id == session_id).first()

    if not session:
        raise ValueError("Session not found")

    if session.status != "finished":
        raise ValueError("Game not finished")

    entry = LeaderboardEntry(
        session_id=session.id,
        player_name=player_name,
        score=session.score,
        mode=session.mode,
        played_at=dt.utcnow()
    )

    db.add(entry)
    db.flush()

    better_count = db.query(LeaderboardEntry).filter(
        LeaderboardEntry.score > entry.score,
        LeaderboardEntry.mode == session.mode
    ).count()

    rank = better_count + 1

    db.commit()

    return SaveLeaderboardResponse(
        message="Saved",
        leaderboard_entry_id=entry.id,
        rank=rank
    )


def get_leaderboard(db: Session, mode: str, limit: int = 50):

    entries = (
        db.query(LeaderboardEntry)
        .filter(LeaderboardEntry.mode == mode)
        .order_by(desc(LeaderboardEntry.score))
        .limit(limit)
        .all()
    )

    items = []

    for i, e in enumerate(entries, start=1):
        items.append(LeaderboardItem(
            rank=i,
            player_name=e.player_name,
            score=e.score,
            mode=e.mode,
            played_at=e.played_at
        ))

    return LeaderboardResponse(items=items)
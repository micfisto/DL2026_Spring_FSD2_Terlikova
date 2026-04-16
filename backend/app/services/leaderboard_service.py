from sqlalchemy.orm import Session

from ..models.leaderboard_entry import LeaderboardEntry
from ..models.game_session import GameSession

from ..schemas.leaderboard import (
    SaveLeaderboardResponse,
    LeaderboardResponse,
    LeaderboardWithUserResponse
)

from ..utils.leaderboard.rank import calculate_rank
from ..utils.leaderboard.mapper import to_leaderboard_item


# ---------------- SAVE ----------------

def save_leaderboard(db: Session, session_id: int, player_name: str):

    session = db.query(GameSession).filter(GameSession.id == session_id).first()

    if not session:
        raise ValueError("Session not found")

    if session.status != "finished":
        raise ValueError("Game not finished yet")

    existing = db.query(LeaderboardEntry).filter(
        LeaderboardEntry.session_id == session_id
    ).first()

    if existing:
        raise ValueError("Already saved to leaderboard")

    entry = LeaderboardEntry(
        session_id=session.id,
        player_name=player_name,
        score=session.score,
        mode=session.mode
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    rank = calculate_rank(db, entry)

    return SaveLeaderboardResponse(
        message="Saved to leaderboard",
        leaderboard_entry_id=entry.id,
        rank=rank
    )



def get_leaderboard(db: Session, mode: str, limit: int = 50):

    entries = (
        db.query(LeaderboardEntry)
        .filter(LeaderboardEntry.mode == mode)
        .order_by(LeaderboardEntry.score.desc())
        .limit(limit)
        .all()
    )

    return {
        "items": [
            to_leaderboard_item(e, i)
            for i, e in enumerate(entries, start=1)
        ]
    }



def get_leaderboard_with_user(db: Session, mode: str, user_entry_id: int = None):

    entries = (
        db.query(LeaderboardEntry)
        .filter(LeaderboardEntry.mode == mode)
        .order_by(LeaderboardEntry.score.desc())
        .all()
    )

    all_items = [
        to_leaderboard_item(e, i)
        for i, e in enumerate(entries, start=1)
    ]

    top_5 = all_items[:5]

    if not user_entry_id:
        return LeaderboardWithUserResponse(
            top_5=top_5,
            user_rank=None,
            user_entry=None,
            neighbors=[],
            total_players=len(entries)
        )

    user_index = next((i for i, e in enumerate(entries) if e.id == user_entry_id), None)

    if user_index is None:
        return LeaderboardWithUserResponse(
            top_5=top_5,
            user_rank=None,
            user_entry=None,
            neighbors=[],
            total_players=len(entries)
        )

    user_entry = entries[user_index]

    user_item = to_leaderboard_item(user_entry, user_index + 1)

    start = max(0, user_index - 2)
    end = min(len(all_items), user_index + 3)

    return LeaderboardWithUserResponse(
        top_5=top_5,
        user_rank=user_index + 1,
        user_entry=user_item,
        neighbors=all_items[start:end],
        total_players=len(entries)
    )
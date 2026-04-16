from sqlalchemy.orm import Session
from ...models.leaderboard_entry import LeaderboardEntry


def calculate_rank(db: Session, entry: LeaderboardEntry) -> int:
    return db.query(LeaderboardEntry).filter(
        LeaderboardEntry.mode == entry.mode,
        LeaderboardEntry.score > entry.score
    ).count() + 1
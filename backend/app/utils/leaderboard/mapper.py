from ...schemas.leaderboard import LeaderboardItem
from ...models.leaderboard_entry import LeaderboardEntry


def to_leaderboard_item(entry: LeaderboardEntry, rank: int) -> LeaderboardItem:
    return LeaderboardItem(
        rank=rank,
        player_name=entry.player_name,
        score=entry.score,
        mode=entry.mode,
        played_at=entry.played_at
    )
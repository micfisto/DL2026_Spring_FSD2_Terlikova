from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SaveLeaderboardRequest(BaseModel):
    session_id: int
    player_name: str = Field(min_length=2, max_length=50)


class SaveLeaderboardResponse(BaseModel):
    message: str
    leaderboard_entry_id: int
    rank: int


class LeaderboardItem(BaseModel):
    rank: int
    player_name: str
    score: int
    mode: str
    played_at: datetime


class LeaderboardResponse(BaseModel):
    items: List[LeaderboardItem]


class LeaderboardWithUserResponse(BaseModel):
    top_5: List[LeaderboardItem]
    user_rank: Optional[int] = None
    user_entry: Optional[LeaderboardItem] = None
    neighbors: List[LeaderboardItem]
    total_players: int
from typing import List
from datetime import datetime

from pydantic import BaseModel, Field# Сохранение результата
class SaveLeaderboardRequest(BaseModel):
    session_id: int
    player_name: str = Field(min_length=1, max_length=50)


# Ответ после сохранения
class SaveLeaderboardResponse(BaseModel):
    message: str
    leaderboard_entry_id: int
    rank: int


# Один элемент рейтинга
class LeaderboardItem(BaseModel):
    rank: int
    player_name: str
    score: int
    mode: str
    played_at: datetime


# Весь рейтинг
class LeaderboardResponse(BaseModel):
    items: List[LeaderboardItem]
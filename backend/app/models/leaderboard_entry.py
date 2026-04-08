import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db import Base


class LeaderboardEntry(Base):
    __tablename__ = 'leaderboard'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)
    player_name = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    mode = Column(String, nullable=False)
    played_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    session = relationship("GameSession", back_populates="leaderboard_entry")
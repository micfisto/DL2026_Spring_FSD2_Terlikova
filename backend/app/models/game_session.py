import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from backend.app.db import Base


class GameSession(Base):
    __tablename__ = 'game_sessions'

    id = Column(Integer, primary_key=True)
    mode = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    total_questions = Column(Integer, nullable=False)
    current_question_index = Column(Integer, nullable=False, default=0)
    score = Column(Integer, nullable=False, default=0)
    status = Column(String, nullable=False, default="active")
    started_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    finished_at = Column(DateTime)
    player_name = Column(String, nullable=True)

    answers = relationship("Answer", back_populates="session")
    leaderboard_entry = relationship("LeaderboardEntry", back_populates="session", uselist=False)
    session_questions = relationship("SessionQuestion", back_populates="session")
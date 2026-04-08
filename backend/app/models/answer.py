from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint

from backend.app.db import Base


class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_lat = Column(Float, nullable=False)
    selected_lng = Column(Float, nullable=False)
    distance_km = Column(Float, nullable=False)
    points_earned = Column(Integer, nullable=False)
    answered_at = Column(DateTime, nullable=False)

    session = relationship("GameSession", back_populates="answers")
    question = relationship("Question", back_populates="answers")

    __table_args__ = (
        UniqueConstraint('session_id', 'question_id', name='uq_session_question'),
    )

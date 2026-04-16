from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from ..db import Base

class SessionQuestion(Base):
    __tablename__ = "session_questions"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('game_sessions.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    order_index = Column(Integer, nullable=False)

    session = relationship("GameSession", back_populates="session_questions")
    question = relationship("Question", back_populates="session_questions")

    __table_args__ = (
        UniqueConstraint("session_id", "order_index", name="uq_session_question_order"),
        UniqueConstraint("session_id", "question_id", name="uq_session_question_once"),
    )
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from backend.app.db import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question_text = Column(String, nullable=False)
    mode=Column(String, nullable=False)
    target_name = Column(String, nullable=False)
    target_type = Column(String, nullable=False)
    correct_lat = Column(Float, nullable=False)
    correct_lng = Column(Float, nullable=False)
    difficulty = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    answers = relationship("Answer", back_populates="question")
    session_questions = relationship("SessionQuestion", back_populates="question")
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class StartGameRequest(BaseModel):
    mode: Literal["capitals", "countries", "landmarks"]
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    question_count: int = Field(default=5, ge=1, le=20)


class ProgressResponse(BaseModel):
    current: int
    total: int


class QuestionResponse(BaseModel):
    question_id: int
    text: str
    target_type: Literal['country', 'capital', 'landmark']
    target_name: Optional[str] = None  # Название страны для режима countries
    correct_country_code: Optional[str] = None  # ISO код страны для проверки границ


class StartGameResponse(BaseModel):
    session_id: int
    question: QuestionResponse
    progress: ProgressResponse
    score: int


class NextQuestionResponse(BaseModel):
    question: QuestionResponse
    progress: ProgressResponse
    score: int


class SubmitAnswerRequest(BaseModel):
    question_id: int
    selected_lat: float = Field(ge=-90, le=90)
    selected_lng: float = Field(ge=-180, le=180)


class SubmitAnswerResponse(BaseModel):
    question_id: int
    correct_lat: float
    correct_lng: float
    distance_km: float
    points_earned: int
    total_score: int
    is_last_question: bool


class GameFinishedResponse(BaseModel):
    game_finished: bool = True
    final_score: int


class FinishGameResponse(BaseModel):
    session_id: int
    status: Literal["active", "finished"]
    answered_questions: int
    total_questions: int
    final_score: int


class GameResultResponse(BaseModel):
    session_id: int
    mode: str
    final_score: int
    answered_questions: int
    total_questions: int
    finished_at: Optional[datetime]
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

# Запрос на запуск новой игры
class StartGameRequest(BaseModel):
    mode: Literal["capitals", "countries", "landmarks"]
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    question_count: int = Field(default=10, ge=1, le=20)

# Прогресс игры
class ProgressResponse(BaseModel):
    current: int
    total: int

# Вопрос, который показывается игроку
class QuestionResponse(BaseModel):
    question_id: int
    text: str
    target_type: str

# Ответ после запуска игры
class StartGameResponse(BaseModel):
    session_id: int
    question: QuestionResponse
    progress: ProgressResponse
    score: int

# Ответ при получении текущего / следующего вопроса
class NextQuestionResponse(BaseModel):
    question: QuestionResponse
    progress: ProgressResponse
    score: int

# Запрос на отправку ответа
class SubmitAnswerRequest(BaseModel):
    question_id: int
    selected_lat: float = Field(ge=-90, le=90)
    selected_lng: float = Field(ge=-180, le=180)

# Ответ после отправки ответа
class SubmitAnswerResponse(BaseModel):
    question_id: int
    correct_lat: float
    correct_lng: float
    distance_km: float
    points_earned: int
    total_score: int
    is_last_question: bool

# Если игра завершилась
class GameFinishedResponse(BaseModel):
    game_finished: bool = True
    final_score: int

# Ответ при досрочном завершении игры
class FinishGameResponse(BaseModel):
    session_id: int
    status: str
    answered_questions: int
    total_questions: int
    final_score: int

# Итог игры
class GameResultResponse(BaseModel):
    session_id: int
    mode: str
    final_score: int
    answered_questions: int
    total_questions: int
    finished_at: Optional[datetime]
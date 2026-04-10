from pydantic import BaseModel

# Отправка ответа игрока
class SubmitAnswerRequest(BaseModel):
    question_id: int
    selected_lat: float
    selected_lng: float

# Результат ответа
class SubmitAnswerResponse(BaseModel):
    question_id: int
    correct_lat: float
    correct_lng: float
    distance_km: float
    points_earned: int
    total_score: int
    is_last_question: bool
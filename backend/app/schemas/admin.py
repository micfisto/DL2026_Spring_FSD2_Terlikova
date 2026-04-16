from pydantic import BaseModel, Field
from typing import Optional, Literal


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class QuestionCreateRequest(BaseModel):
    question_text: str
    mode: Literal['capitals', 'countries', 'landmarks']
    target_name: str
    target_type: Literal['country', 'capital', 'landmark']
    correct_lat: float = Field(ge=-90, le=90)
    correct_lng: float = Field(ge=-180, le=180)
    difficulty: Literal['easy', 'medium', 'hard']
    is_active: bool = True


class QuestionUpdateRequest(BaseModel):
    question_text: Optional[str] = None
    mode: Optional[Literal['capitals', 'countries', 'landmarks']] = None
    target_name: Optional[str] = None
    target_type: Optional[Literal['country', 'capital', 'landmark']] = None
    correct_lat: Optional[float] = Field(default=None, ge=-90, le=90)
    correct_lng: Optional[float] = Field(default=None, ge=-180, le=180)
    difficulty: Optional[Literal['easy', 'medium', 'hard']] = None
    is_active: Optional[bool] = None
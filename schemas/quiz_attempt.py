# app/schemas/quiz_attempt.py

from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime

class QuizAttemptBase(BaseModel):
    user_id: int
    quiz_id: int

class QuizAttemptCreate(QuizAttemptBase):
    pass

class QuizAttempt(QuizAttemptBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class QuizAttemptResponse(BaseModel):
    data: QuizAttempt

    model_config = ConfigDict(from_attributes=True)

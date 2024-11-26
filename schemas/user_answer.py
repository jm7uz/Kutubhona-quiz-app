# app/schemas/user_answer.py

from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserAnswerBase(BaseModel):
    quiz_attempt_id: int
    question_id: int
    selected_answer_id: int

class UserAnswerCreate(UserAnswerBase):
    pass

class UserAnswer(UserAnswerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserAnswerResponse(BaseModel):
    data: UserAnswer

    model_config = ConfigDict(from_attributes=True)

# app/schemas/answer.py

from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class AnswerBase(BaseModel):
    text: str
    is_correct: bool = False

class AnswerCreate(AnswerBase):
    pass

class AnswerUpdate(BaseModel):
    text: Optional[str] = None
    is_correct: Optional[bool] = None

class Answer(AnswerBase):
    id: int
    question_id: int

    model_config = ConfigDict(from_attributes=True)

class AnswerResponse(BaseModel):
    data: Answer

    model_config = ConfigDict(from_attributes=True)

# app/schemas/question.py

from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class QuestionBase(BaseModel):
    text: str

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    text: Optional[str] = None

class Question(QuestionBase):
    id: int
    quiz_id: int

    model_config = ConfigDict(from_attributes=True)

class QuestionResponse(BaseModel):
    data: Question

    model_config = ConfigDict(from_attributes=True)

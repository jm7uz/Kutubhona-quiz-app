# app/schemas/quiz.py

from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class QuizBase(BaseModel):
    title: str

class QuizCreate(QuizBase):
    pass

class QuizUpdate(QuizBase):
    pass

class Quiz(QuizBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class QuizResponse(BaseModel):
    data: Quiz

    model_config = ConfigDict(from_attributes=True)

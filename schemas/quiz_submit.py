# app/schemas/quiz_submit.py

from pydantic import BaseModel
from typing import List

class QuizSubmitAnswer(BaseModel):
    question_id: int
    selected_answer_id: int

class QuizSubmit(BaseModel):
    attempt_id: int
    answers: List[QuizSubmitAnswer]

class QuizResult(BaseModel):
    total: int
    correct: int

class QuizSubmitResponse(BaseModel):
    data: QuizResult

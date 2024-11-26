# app/routers/quizzes.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.quiz import (
    QuizResponse,
    QuizCreate,
    Quiz,
    QuizUpdate,
)
from app.schemas.question import (
    QuestionResponse,
    QuestionCreate,
    Question,
    QuestionUpdate,
)
from app.schemas.answer import (
    AnswerResponse,
    AnswerCreate,
    Answer,
    AnswerUpdate,
)
from app.schemas.quiz_attempt import (
    QuizAttemptResponse,
    QuizAttemptCreate,
    QuizAttempt,
)
from app.schemas.quiz_submit import QuizSubmit, QuizSubmitResponse
from app.schemas.user_answer import (
    UserAnswerResponse,
    UserAnswerCreate,
    UserAnswer,
)
from app import crud, models, schemas
from app.database import SessionLocal
from random import sample

router = APIRouter(
    prefix="/v1/quizzes",
    tags=["Quizzes"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### Quiz CRUD Operations

@router.get("/", response_model=List[Quiz])
def read_quizzes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    quizzes = crud.get_quizzes(db, skip=skip, limit=limit)
    return quizzes

@router.get("/{quiz_id}", response_model=Quiz)
def read_quiz(quiz_id: int, db: Session = Depends(get_db)):
    db_quiz = crud.get_quiz(db, quiz_id=quiz_id)
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz

@router.post("/", response_model=Quiz, status_code=201)
def create_new_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):
    db_quiz = crud.get_quiz(db, quiz_id=0)  # Dummy call to avoid IDE error
    db_quiz = crud.create_quiz(db, quiz=quiz)
    return db_quiz

@router.put("/{quiz_id}", response_model=Quiz)
def update_existing_quiz(quiz_id: int, quiz: QuizUpdate, db: Session = Depends(get_db)):
    db_quiz = crud.update_quiz(db, quiz_id=quiz_id, quiz=quiz)
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_quiz

@router.delete("/{quiz_id}", status_code=204)
def delete_existing_quiz(quiz_id: int, db: Session = Depends(get_db)):
    success = crud.delete_quiz(db, quiz_id=quiz_id)
    if not success:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return

### Question CRUD Operations

@router.get("/{quiz_id}/questions", response_model=List[Question])
def read_questions(quiz_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_quiz = crud.get_quiz(db, quiz_id=quiz_id)
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    questions = crud.get_questions(db, skip=skip, limit=limit)
    return questions

@router.get("/{quiz_id}/questions/{question_id}", response_model=Question)
def read_question(quiz_id: int, question_id: int, db: Session = Depends(get_db)):
    db_question = crud.get_question(db, question_id=question_id)
    if not db_question or db_question.quiz_id != quiz_id:
        raise HTTPException(status_code=404, detail="Question not found in the specified quiz")
    return db_question

@router.post("/{quiz_id}/questions", response_model=Question, status_code=201)
def create_new_question(quiz_id: int, question: QuestionCreate, db: Session = Depends(get_db)):
    db_quiz = crud.get_quiz(db, quiz_id=quiz_id)
    if not db_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    db_question = crud.create_question(db, question=question, quiz_id=quiz_id)
    return db_question

@router.put("/{quiz_id}/questions/{question_id}", response_model=Question)
def update_existing_question(quiz_id: int, question_id: int, question: QuestionUpdate, db: Session = Depends(get_db)):
    db_question = crud.get_question(db, question_id=question_id)
    if not db_question or db_question.quiz_id != quiz_id:
        raise HTTPException(status_code=404, detail="Question not found in the specified quiz")
    db_question = crud.update_question(db, question_id=question_id, question=question)
    return db_question

@router.delete("/{quiz_id}/questions/{question_id}", status_code=204)
def delete_existing_question(quiz_id: int, question_id: int, db: Session = Depends(get_db)):
    db_question = crud.get_question(db, question_id=question_id)
    if not db_question or db_question.quiz_id != quiz_id:
        raise HTTPException(status_code=404, detail="Question not found in the specified quiz")
    success = crud.delete_question(db, question_id=question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return

### Answer CRUD Operations

@router.get("/{quiz_id}/questions/{question_id}/answers", response_model=List[Answer])
def read_answers(quiz_id: int, question_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_question = crud.get_question(db, question_id=question_id)
    if not db_question or db_question.quiz_id != quiz_id:
        raise HTTPException(status_code=404, detail="Question not found in the specified quiz")
    answers = crud.get_answers(db, skip=skip, limit=limit)
    return answers

@router.get("/{quiz_id}/questions/{question_id}/answers/{answer_id}", response_model=Answer)
def read_answer(quiz_id: int, question_id: int, answer_id: int, db: Session = Depends(get_db)):
    db_answer = crud.get_answer(db, answer_id=answer_id)
    if not db_answer or db_answer.question_id != question_id:
        raise HTTPException(status_code=404, detail="Answer not found in the specified question")
    return db_answer

@router.post("/{quiz_id}/questions/{question_id}/answers", response_model=Answer, status_code=201)
def create_new_answer(quiz_id: int, question_id: int, answer: AnswerCreate, db: Session = Depends(get_db)):
    db_question = crud.get_question(db, question_id=question_id)
    if not db_question or db_question.quiz_id != quiz_id:
        raise HTTPException(status_code=404, detail="Question not found in the specified quiz")
    db_answer = crud.create_answer(db, answer=answer, question_id=question_id)
    return db_answer

@router.put("/{quiz_id}/questions/{question_id}/answers/{answer_id}", response_model=Answer)
def update_existing_answer(quiz_id: int, question_id: int, answer_id: int, answer: AnswerUpdate, db: Session = Depends(get_db)):
    db_answer = crud.get_answer(db, answer_id=answer_id)
    if not db_answer or db_answer.question_id != question_id:
        raise HTTPException(status_code=404, detail="Answer not found in the specified question")
    db_answer = crud.update_answer(db, answer_id=answer_id, answer=answer)
    return db_answer

@router.delete("/{quiz_id}/questions/{question_id}/answers/{answer_id}", status_code=204)
def delete_existing_answer(quiz_id: int, question_id: int, answer_id: int, db: Session = Depends(get_db)):
    db_answer = crud.get_answer(db, answer_id=answer_id)
    if not db_answer or db_answer.question_id != question_id:
        raise HTTPException(status_code=404, detail="Answer not found in the specified question")
    success = crud.delete_answer(db, answer_id=answer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Answer not found")
    return


from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.quiz import (
    QuizResponse,
    QuizCreate,
    Quiz,
    QuizUpdate,
)
from app.schemas.question import (
    QuestionResponse,
    QuestionCreate,
    Question,
    QuestionUpdate,
)
from app.schemas.answer import (
    AnswerResponse,
    AnswerCreate,
    Answer,
    AnswerUpdate,
)
from app.schemas.quiz_attempt import (
    QuizAttemptResponse,
    QuizAttemptCreate,
    QuizAttempt,
)
from app.schemas.user_answer import (
    UserAnswerResponse,
    UserAnswerCreate,
    UserAnswer,
)
from app import crud
from app.database import SessionLocal
from random import sample
from pydantic import BaseModel

class QuizResult(BaseModel):
    data: dict

@router.post("/{quiz_id}/attempts", response_model=QuizAttemptResponse, status_code=201)
def create_quiz_attempt(quiz_id: int, attempt: QuizAttemptCreate, db: Session = Depends(get_db)):
    # Foydalanuvchi bu quizni oldin yechganligini tekshirish
    existing_attempt = crud.quiz_attempt.get_user_quiz_attempt(db, user_id=attempt.user_id, quiz_id=quiz_id)
    if existing_attempt:
        raise HTTPException(status_code=400, detail="User has already attempted this quiz.")
    
    # Yangi urinish yaratish
    db_attempt = crud.quiz_attempt.create_quiz_attempt(db, attempt=attempt)
    if not db_attempt:
        raise HTTPException(status_code=400, detail="User has already attempted this quiz.")
    
    # Savollarni olish va javoblarni tashqi API yoki boshqa logikaga asoslangan holda tanlash kerak
    # Bu yerda misol uchun barcha savollar va javoblarni qaytaramiz
    questions = db.query(models.Question).filter(models.Question.quiz_id == quiz_id).all()
    questions_data = []
    for question in questions:
        answers = db.query(models.Answer).filter(models.Answer.question_id == question.id).all()
        answers_data = [{"id": ans.id, "text": ans.text} for ans in answers]
        questions_data.append({
            "question_id": question.id,
            "text": question.text,
            "answers": answers_data
        })
    
    return QuizAttemptResponse(
        data={
            "quiz_id": quiz_id,
            "attempt_id": db_attempt.id,
            "questions": questions_data
        }
    )

class SubmitQuiz(BaseModel):
    attempt_id: int
    answers: List[dict]  # [{"question_id": int, "selected_answer_id": int}, ...]

@router.post("/submit", response_model=QuizSubmitResponse)
def submit_quiz(submission: QuizSubmit, db: Session = Depends(get_db)):
    result = crud.quiz_attempt.submit_quiz(db, submission=submission)
    if not result:
        raise HTTPException(status_code=404, detail="Quiz attempt not found.")
    return QuizSubmitResponse(data=result)
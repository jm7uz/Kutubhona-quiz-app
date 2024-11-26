# app/crud/quiz_attempt.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from sqlalchemy.exc import IntegrityError
from app.schemas import QuizSubmit, QuizResult  # Qo'shish kerak

def get_quiz_attempts(db: Session, skip: int = 0, limit: int = 100) -> List[models.QuizAttempt]:
    return db.query(models.QuizAttempt).offset(skip).limit(limit).all()

def get_quiz_attempt(db: Session, attempt_id: int) -> Optional[models.QuizAttempt]:
    return db.query(models.QuizAttempt).filter(models.QuizAttempt.id == attempt_id).first()

def get_user_quiz_attempt(db: Session, user_id: int, quiz_id: int) -> Optional[models.QuizAttempt]:
    return db.query(models.QuizAttempt).filter(
        models.QuizAttempt.user_id == user_id,
        models.QuizAttempt.quiz_id == quiz_id
    ).first()

def create_quiz_attempt(db: Session, attempt: schemas.QuizAttemptCreate) -> Optional[models.QuizAttempt]:
    db_attempt = models.QuizAttempt(user_id=attempt.user_id, quiz_id=attempt.quiz_id)
    db.add(db_attempt)
    try:
        db.commit()
        db.refresh(db_attempt)
        return db_attempt
    except IntegrityError:
        db.rollback()
        return None  # Foydalanuvchi bu quizni oldin yechgan

def delete_quiz_attempt(db: Session, attempt_id: int) -> bool:
    db_attempt = get_quiz_attempt(db, attempt_id)
    if db_attempt:
        db.delete(db_attempt)
        db.commit()
        return True
    return False

def submit_quiz(db: Session, submission: QuizSubmit) -> Optional[QuizResult]:
    db_attempt = get_quiz_attempt(db, submission.attempt_id)
    if not db_attempt:
        return None

    # Javoblarni tekshirish va to'g'ri javoblar sonini hisoblash
    correct_answers = 0
    total_questions = len(submission.answers)

    for ans in submission.answers:
        question = db.query(models.Question).filter(models.Question.id == ans.question_id).first()
        if not question:
            continue
        selected_answer = db.query(models.Answer).filter(
            models.Answer.id == ans.selected_answer_id,
            models.Answer.question_id == ans.question_id
        ).first()
        if not selected_answer:
            continue
        db_user_answer = models.UserAnswer(
            quiz_attempt_id=submission.attempt_id,
            question_id=ans.question_id,
            selected_answer_id=ans.selected_answer_id
        )
        db.add(db_user_answer)
        if selected_answer.is_correct:
            correct_answers += 1

    db.commit()

    # Foydalanuvchining balini yangilash
    db_user = db.query(models.User).filter(models.User.id == db_attempt.user_id).first()
    if db_user:
        db_user.bal += correct_answers
        db.commit()

    return QuizResult(total=total_questions, correct=correct_answers)

# app/crud/quiz.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas

def get_quizzes(db: Session, skip: int = 0, limit: int = 100) -> List[models.Quiz]:
    return db.query(models.Quiz).offset(skip).limit(limit).all()

def get_quiz(db: Session, quiz_id: int) -> Optional[models.Quiz]:
    return db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()

def create_quiz(db: Session, quiz: schemas.QuizCreate) -> models.Quiz:
    db_quiz = models.Quiz(title=quiz.title)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

def update_quiz(db: Session, quiz_id: int, quiz: schemas.QuizUpdate) -> Optional[models.Quiz]:
    db_quiz = get_quiz(db, quiz_id)
    if db_quiz:
        db_quiz.title = quiz.title
        db.commit()
        db.refresh(db_quiz)
    return db_quiz

def delete_quiz(db: Session, quiz_id: int) -> bool:
    db_quiz = get_quiz(db, quiz_id)
    if db_quiz:
        db.delete(db_quiz)
        db.commit()
        return True
    return False

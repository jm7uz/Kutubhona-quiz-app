# app/crud/question.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas

def get_questions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Question]:
    return db.query(models.Question).offset(skip).limit(limit).all()

def get_question(db: Session, question_id: int) -> Optional[models.Question]:
    return db.query(models.Question).filter(models.Question.id == question_id).first()

def create_question(db: Session, question: schemas.QuestionCreate, quiz_id: int) -> models.Question:
    db_question = models.Question(
        text=question.text,
        quiz_id=quiz_id
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def update_question(db: Session, question_id: int, question: schemas.QuestionUpdate) -> Optional[models.Question]:
    db_question = get_question(db, question_id)
    if db_question:
        if question.text:
            db_question.text = question.text
        db.commit()
        db.refresh(db_question)
    return db_question

def delete_question(db: Session, question_id: int) -> bool:
    db_question = get_question(db, question_id)
    if db_question:
        db.delete(db_question)
        db.commit()
        return True
    return False

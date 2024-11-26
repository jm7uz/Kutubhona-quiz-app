# app/crud/user_answer.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas

def get_user_answers(db: Session, skip: int = 0, limit: int = 100) -> List[models.UserAnswer]:
    return db.query(models.UserAnswer).offset(skip).limit(limit).all()

def get_user_answer(db: Session, answer_id: int) -> Optional[models.UserAnswer]:
    return db.query(models.UserAnswer).filter(models.UserAnswer.id == answer_id).first()

def create_user_answer(db: Session, user_answer: schemas.UserAnswerCreate) -> models.UserAnswer:
    db_user_answer = models.UserAnswer(
        quiz_attempt_id=user_answer.quiz_attempt_id,
        question_id=user_answer.question_id,
        selected_answer_id=user_answer.selected_answer_id
    )
    db.add(db_user_answer)
    db.commit()
    db.refresh(db_user_answer)
    return db_user_answer

def update_user_answer(db: Session, answer_id: int, user_answer: schemas.UserAnswerCreate) -> Optional[models.UserAnswer]:
    db_user_answer = get_user_answer(db, answer_id)
    if db_user_answer:
        db_user_answer.quiz_attempt_id = user_answer.quiz_attempt_id
        db_user_answer.question_id = user_answer.question_id
        db_user_answer.selected_answer_id = user_answer.selected_answer_id
        db.commit()
        db.refresh(db_user_answer)
    return db_user_answer

def delete_user_answer(db: Session, answer_id: int) -> bool:
    db_user_answer = get_user_answer(db, answer_id)
    if db_user_answer:
        db.delete(db_user_answer)
        db.commit()
        return True
    return False

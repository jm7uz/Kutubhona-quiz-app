# app/crud/answer.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas

def get_answers(db: Session, skip: int = 0, limit: int = 100) -> List[models.Answer]:
    return db.query(models.Answer).offset(skip).limit(limit).all()

def get_answer(db: Session, answer_id: int) -> Optional[models.Answer]:
    return db.query(models.Answer).filter(models.Answer.id == answer_id).first()

def create_answer(db: Session, answer: schemas.AnswerCreate, question_id: int) -> models.Answer:
    db_answer = models.Answer(
        text=answer.text,
        is_correct=answer.is_correct,
        question_id=question_id
    )
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer

def update_answer(db: Session, answer_id: int, answer: schemas.AnswerUpdate) -> Optional[models.Answer]:
    db_answer = get_answer(db, answer_id)
    if db_answer:
        if answer.text:
            db_answer.text = answer.text
        if answer.is_correct is not None:
            db_answer.is_correct = answer.is_correct
        db.commit()
        db.refresh(db_answer)
    return db_answer

def delete_answer(db: Session, answer_id: int) -> bool:
    db_answer = get_answer(db, answer_id)
    if db_answer:
        db.delete(db_answer)
        db.commit()
        return True
    return False

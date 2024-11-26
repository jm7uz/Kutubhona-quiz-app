# app/crud/user.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_telegram_id(db: Session, telegram_id: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        telegram_id=user.telegram_id,
        username=user.username,
        full_name=user.full_name,
        password=hashed_password,
        region_id=user.region_id,
        district_id=user.district_id,
        organization_id=user.organization_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> Optional[models.User]:
    db_user = get_user(db, user_id)
    if db_user:
        if user.telegram_id:
            db_user.telegram_id = user.telegram_id
        if user.username:
            db_user.username = user.username
        if user.full_name:
            db_user.full_name = user.full_name
        if user.password:
            db_user.password = pwd_context.hash(user.password)
        if user.region_id is not None:
            db_user.region_id = user.region_id
        if user.district_id is not None:
            db_user.district_id = user.district_id
        if user.organization_id is not None:
            db_user.organization_id = user.organization_id
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

def authenticate_user(db: Session, username: str, password: str) -> Optional[models.User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not pwd_context.verify(password, user.password):
        return None
    return user

def update_user_bal(db: Session, user_id: int, bal: int) -> Optional[models.User]:
    db_user = get_user(db, user_id)
    if db_user:
        db_user.bal += bal
        db.commit()
        db.refresh(db_user)
    return db_user

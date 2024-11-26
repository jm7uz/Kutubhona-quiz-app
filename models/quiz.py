# app/models/quiz.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")

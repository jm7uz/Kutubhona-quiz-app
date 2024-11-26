# app/models/user_answer.py

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class UserAnswer(Base):
    __tablename__ = "user_answers"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_answer_id = Column(Integer, ForeignKey("answers.id"), nullable=False)
    
    quiz_attempt = relationship("QuizAttempt", back_populates="user_answers")
    question = relationship("Question")
    selected_answer = relationship("Answer")

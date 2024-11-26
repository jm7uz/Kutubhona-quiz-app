# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Yangi ma'lumotlar bazasi URL'sini belgilash
SQLALCHEMY_DATABASE_URL = "sqlite:///./quiz.db"  # oldingi "sqlite:///./test.db" ni o'zgartiring

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Debug uchun qo'shing
print(f"Using database at: {os.path.abspath('quiz.db')}")

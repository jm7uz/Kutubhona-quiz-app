# app/main.py

from fastapi import FastAPI
from app.database import engine, Base
from app.routers import regions, districts, organizations, users, quizzes


app = FastAPI(
    title="Regions, Districts, Organizations and Quiz API",
    version="1.1.0",
    description="API for managing regions, districts, organizations and quizzes."
)

app.include_router(regions.router)
app.include_router(districts.router)
app.include_router(organizations.router)
app.include_router(users.router)
app.include_router(quizzes.router)
# app/schemas/user.py

from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    telegram_id: str
    username: str
    full_name: str
    region_id: Optional[int] = None
    district_id: Optional[int] = None
    organization_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    telegram_id: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    region_id: Optional[int] = None
    district_id: Optional[int] = None
    organization_id: Optional[int] = None

class User(UserBase):
    id: int
    bal: int  # Yangi bal maydoni
    
    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    data: User

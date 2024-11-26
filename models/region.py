# app/models/region.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Region(Base):
    __tablename__ = "regions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    
    districts = relationship("District", back_populates="region", cascade="all, delete-orphan")
    organizations = relationship("Organization", back_populates="region", cascade="all, delete-orphan")

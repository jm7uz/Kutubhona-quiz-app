# app/models/organization.py

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class OrganizationType(str, enum.Enum):
    university = "University"
    kollej = "Kollej"
    schools = "Schools"
    other = "Other"

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    type = Column(Enum(OrganizationType), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    
    region = relationship("Region", back_populates="organizations")

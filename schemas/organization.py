# app/schemas/organization.py

from pydantic import BaseModel, ConfigDict
from typing import List
from enum import Enum

class OrganizationType(str, Enum):
    university = "University"
    kollej = "Kollej"
    schools = "Schools"
    other = "Other"

class OrganizationBase(BaseModel):
    title: str
    type: OrganizationType

class OrganizationCreate(OrganizationBase):
    region_id: int

class OrganizationUpdate(BaseModel):
    title: str
    type: OrganizationType
    region_id: int

class Organization(OrganizationBase):
    id: int
    region_id: int

    model_config = ConfigDict(from_attributes=True)

class OrganizationResponse(BaseModel):
    data: List[Organization]

    model_config = ConfigDict(from_attributes=True)

# app/schemas/region.py

from pydantic import BaseModel

class RegionBase(BaseModel):
    id: int
    name: str

class RegionCreate(RegionBase):
    pass

class RegionUpdate(BaseModel):
    name: str

class RegionResponse(RegionBase):
    id: int

    class Config:
        orm_mode = True

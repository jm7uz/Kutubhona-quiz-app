# app/schemas/district.py

from pydantic import BaseModel, ConfigDict
from typing import List

class DistrictBase(BaseModel):
    name: str

class DistrictCreate(DistrictBase):
    id : int
    region_id: int

class DistrictUpdate(DistrictBase):
    region_id: int

class District(DistrictBase):
    id: int
    region_id: int

    model_config = ConfigDict(from_attributes=True)

class DistrictResponse(BaseModel):
    data: List[District]

    model_config = ConfigDict(from_attributes=True)

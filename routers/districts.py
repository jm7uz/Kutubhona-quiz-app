# app/routers/districts.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.district import (
    DistrictResponse,
    DistrictCreate,
    District,
    DistrictUpdate,
)
from app import crud
from app.database import SessionLocal

router = APIRouter(
    prefix="/v1/users/regions/{region_id}/districts",
    tags=["Districts"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=DistrictResponse)
def read_districts(region_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_region = crud.region.get_region(db, region_id=region_id)
    if not db_region:
        raise HTTPException(status_code=404, detail="Region not found")
    districts = crud.district.get_districts_by_region(db, region_id=region_id, skip=skip, limit=limit)
    return {"data": districts}

@router.get("/{district_id}", response_model=District)
def read_district(region_id: int, district_id: int, db: Session = Depends(get_db)):
    db_district = crud.district.get_district(db, district_id=district_id)
    if not db_district or db_district.region_id != region_id:
        raise HTTPException(status_code=404, detail="District not found in the specified region")
    return db_district

@router.post("/", response_model=District, status_code=201)
def create_new_district(region_id: int, district: DistrictCreate, db: Session = Depends(get_db)):
    db_region = crud.region.get_region(db, region_id=region_id)
    if not db_region:
        raise HTTPException(status_code=404, detail="Region not found")
    district.region_id = region_id
    db_district = crud.district.create_district(db, district=district)
    return db_district

@router.put("/{district_id}", response_model=District)
def update_existing_district(region_id: int, district_id: int, district: DistrictUpdate, db: Session = Depends(get_db)):
    db_district = crud.district.get_district(db, district_id=district_id)
    if not db_district or db_district.region_id != region_id:
        raise HTTPException(status_code=404, detail="District not found in the specified region")
    db_district = crud.district.update_district(db, district_id=district_id, district=district)
    return db_district

@router.delete("/{district_id}", status_code=204)
def delete_existing_district(region_id: int, district_id: int, db: Session = Depends(get_db)):
    db_district = crud.district.get_district(db, district_id=district_id)
    if not db_district or db_district.region_id != region_id:
        raise HTTPException(status_code=404, detail="District not found in the specified region")
    success = crud.district.delete_district(db, district_id=district_id)
    if not success:
        raise HTTPException(status_code=404, detail="District not found")
    return

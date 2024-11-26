# app/routers/regions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.region import (
    RegionResponse,
    RegionCreate,
    RegionUpdate,
)
from app import crud
from app.database import SessionLocal

router = APIRouter(
    prefix="/v1/regions",  # Agar regions foydalanuvchilar bilan bog'liq bo'lmasa, "/v1/users/regions" emas "/v1/regions" bo'lishi kerak
    tags=["Regions"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Barcha regionlarni olish
@router.get("/", response_model=List[RegionResponse])
def read_regions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    regions = crud.region.get_regions(db, skip=skip, limit=limit)
    return regions

# Bitta regionni olish
@router.get("/{region_id}", response_model=RegionResponse)
def read_region(region_id: int, db: Session = Depends(get_db)):
    db_region = crud.region.get_region(db, region_id=region_id)
    if not db_region:
        raise HTTPException(status_code=404, detail="Region not found")
    return db_region

# Yangi region yaratish
@router.post("/", response_model=RegionResponse, status_code=201)
def create_new_region(region: RegionCreate, db: Session = Depends(get_db)):
    db_region = crud.region.create_region(db, region=region)
    return db_region

# Regionni yangilash
@router.put("/{region_id}", response_model=RegionResponse)
def update_existing_region(region_id: int, region: RegionUpdate, db: Session = Depends(get_db)):
    db_region = crud.region.update_region(db, region_id=region_id, region=region)
    if not db_region:
        raise HTTPException(status_code=404, detail="Region not found")
    return db_region

# Regionni o'chirish
@router.delete("/{region_id}", status_code=204)
def delete_existing_region(region_id: int, db: Session = Depends(get_db)):
    success = crud.region.delete_region(db, region_id=region_id)
    if not success:
        raise HTTPException(status_code=404, detail="Region not found")
    return

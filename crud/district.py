# app/crud/district.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas

def get_districts(db: Session, skip: int = 0, limit: int = 100) -> List[models.District]:
    return db.query(models.District).offset(skip).limit(limit).all()

def get_district(db: Session, district_id: int) -> Optional[models.District]:
    return db.query(models.District).filter(models.District.id == district_id).first()

def get_districts_by_region(db: Session, region_id: int, skip: int = 0, limit: int = 100) -> List[models.District]:
    return db.query(models.District).filter(models.District.region_id == region_id).offset(skip).limit(limit).all()

def create_district(db: Session, district: schemas.DistrictCreate) -> models.District:
    db_district = models.District(name=district.name, region_id=district.region_id, id = district.id)
    db.add(db_district)
    db.commit()
    db.refresh(db_district)
    return db_district

def update_district(db: Session, district_id: int, district: schemas.DistrictUpdate) -> Optional[models.District]:
    db_district = get_district(db, district_id)
    if db_district:
        db_district.name = district.name
        db_district.region_id = district.region_id
        db.commit()
        db.refresh(db_district)
    return db_district

def delete_district(db: Session, district_id: int) -> bool:
    db_district = get_district(db, district_id)
    if db_district:
        db.delete(db_district)
        db.commit()
        return True
    return False

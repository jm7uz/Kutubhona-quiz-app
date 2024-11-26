# app/crud/region.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas

def get_regions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Region]:
    return db.query(models.Region).offset(skip).limit(limit).all()

def get_region(db: Session, region_id: int) -> Optional[models.Region]:
    return db.query(models.Region).filter(models.Region.id == region_id).first()

def create_region(db: Session, region: schemas.RegionCreate) -> models.Region:
    db_region = models.Region(name=region.name, id = region.id)
    db.add(db_region)
    db.commit()
    db.refresh(db_region)
    return db_region

def update_region(db: Session, region_id: int, region: schemas.RegionUpdate) -> Optional[models.Region]:
    db_region = get_region(db, region_id)
    if db_region:
        db_region.name = region.name
        db.commit()
        db.refresh(db_region)
    return db_region

def delete_region(db: Session, region_id: int) -> bool:
    db_region = get_region(db, region_id)
    if db_region:
        db.delete(db_region)
        db.commit()
        return True
    return False

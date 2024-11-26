# app/crud/organization.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas

def get_organizations(db: Session, skip: int = 0, limit: int = 100) -> List[models.Organization]:
    return db.query(models.Organization).offset(skip).limit(limit).all()

def get_organization(db: Session, organization_id: int) -> Optional[models.Organization]:
    return db.query(models.Organization).filter(models.Organization.id == organization_id).first()

def get_organizations_by_region(db: Session, region_id: int, skip: int = 0, limit: int = 100) -> List[models.Organization]:
    return db.query(models.Organization).filter(models.Organization.region_id == region_id).offset(skip).limit(limit).all()

def get_organizations_by_region_and_type(
    db: Session, region_id: int, org_type: schemas.OrganizationType, skip: int = 0, limit: int = 100
) -> List[models.Organization]:
    return db.query(models.Organization).filter(
        models.Organization.region_id == region_id,
        models.Organization.type == org_type
    ).offset(skip).limit(limit).all()

def create_organization(db: Session, organization: schemas.OrganizationCreate) -> models.Organization:
    db_organization = models.Organization(
        title=organization.title,
        type=organization.type,
        region_id=organization.region_id
    )
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization

def update_organization(db: Session, organization_id: int, organization: schemas.OrganizationUpdate) -> Optional[models.Organization]:
    db_organization = get_organization(db, organization_id)
    if db_organization:
        db_organization.title = organization.title
        db_organization.type = organization.type
        db_organization.region_id = organization.region_id
        db.commit()
        db.refresh(db_organization)
    return db_organization

def delete_organization(db: Session, organization_id: int) -> bool:
    db_organization = get_organization(db, organization_id)
    if db_organization:
        db.delete(db_organization)
        db.commit()
        return True
    return False

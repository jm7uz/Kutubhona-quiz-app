# app/routers/organizations.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.organization import (
    OrganizationResponse,
    OrganizationCreate,
    Organization,
    OrganizationUpdate,
    OrganizationType,
)
from app import crud
from app.database import SessionLocal

router = APIRouter(
    prefix="/v1/users/regions/{region_id}/organizations",
    tags=["Organizations"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=OrganizationResponse)
def read_organizations(
    region_id: int,
    org_type: Optional[OrganizationType] = Query(None, description="Filter by organization type"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    db_region = crud.region.get_region(db, region_id=region_id)
    if not db_region:
        raise HTTPException(status_code=404, detail="Region not found")
    if org_type:
        organizations = crud.organization.get_organizations_by_region_and_type(
            db, region_id=region_id, org_type=org_type, skip=skip, limit=limit
        )
    else:
        organizations = crud.organization.get_organizations_by_region(
            db, region_id=region_id, skip=skip, limit=limit
        )
    return {"data": organizations}

@router.get("/{organization_id}", response_model=Organization)
def read_organization(region_id: int, organization_id: int, db: Session = Depends(get_db)):
    db_organization = crud.organization.get_organization(db, organization_id=organization_id)
    if not db_organization or db_organization.region_id != region_id:
        raise HTTPException(status_code=404, detail="Organization not found in the specified region")
    return db_organization

@router.post("/", response_model=Organization, status_code=201)
def create_new_organization(region_id: int, organization: OrganizationCreate, db: Session = Depends(get_db)):
    db_region = crud.region.get_region(db, region_id=region_id)
    if not db_region:
        raise HTTPException(status_code=404, detail="Region not found")
    organization.region_id = region_id
    db_organization = crud.organization.create_organization(db, organization=organization)
    return db_organization

@router.put("/{organization_id}", response_model=Organization)
def update_existing_organization(
    region_id: int,
    organization_id: int,
    organization: OrganizationUpdate,
    db: Session = Depends(get_db)
):
    db_organization = crud.organization.get_organization(db, organization_id=organization_id)
    if not db_organization or db_organization.region_id != region_id:
        raise HTTPException(status_code=404, detail="Organization not found in the specified region")
    db_organization = crud.organization.update_organization(db, organization_id=organization_id, organization=organization)
    return db_organization

@router.delete("/{organization_id}", status_code=204)
def delete_existing_organization(region_id: int, organization_id: int, db: Session = Depends(get_db)):
    db_organization = crud.organization.get_organization(db, organization_id=organization_id)
    if not db_organization or db_organization.region_id != region_id:
        raise HTTPException(status_code=404, detail="Organization not found in the specified region")
    success = crud.organization.delete_organization(db, organization_id=organization_id)
    if not success:
        raise HTTPException(status_code=404, detail="Organization not found")
    return

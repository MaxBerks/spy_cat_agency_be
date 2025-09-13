from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/api/cats", tags=["cats"])

@router.post("", response_model=schemas.SpyCatResponse, status_code=status.HTTP_201_CREATED)
def create_cat(payload: schemas.SpyCatCreate, db: Session = Depends(get_db)):
    cat = models.SpyCat(**payload.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

@router.get("", response_model=List[schemas.SpyCatResponse])
def list_cats(db: Session = Depends(get_db)):
    return db.query(models.SpyCat).all()

@router.get("/{cat_id}", response_model=schemas.SpyCatResponse)
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(models.SpyCat).filter(models.SpyCat.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Spy cat not found")
    return cat

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/api/missions", tags=["missions"])

@router.post("", response_model=schemas.MissionResponse, status_code=status.HTTP_201_CREATED)
def create_mission(payload: schemas.MissionCreate, db: Session = Depends(get_db)):
    if payload.cat_id is not None:
        cat = db.query(models.SpyCat).filter(models.SpyCat.id == payload.cat_id).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Spy cat not found")
        existing = db.query(models.Mission).filter(
            models.Mission.cat_id == payload.cat_id,
            models.Mission.is_complete == False
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Cat already has an active mission")

    mission = models.Mission(cat_id=payload.cat_id, is_complete=False)
    db.add(mission)
    db.flush()  

    for t in payload.targets:
        target = models.Target(
            mission_id=mission.id,
            name=t.name,
            country=t.country,
            notes=t.notes,
            is_complete=t.is_complete,
        )
        db.add(target)

    db.commit()
    db.refresh(mission)
    return mission

@router.get("", response_model=List[schemas.MissionResponse])
def list_missions(db: Session = Depends(get_db)):
    return db.query(models.Mission).all()

@router.get("/{mission_id}", response_model=schemas.MissionResponse)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if mission.cat_id is not None:
        raise HTTPException(status_code=400, detail="Cannot delete mission assigned to a cat")
    db.delete(mission)
    db.commit()

@router.patch("/{mission_id}/assign", response_model=schemas.MissionResponse)
def assign_cat(mission_id: int, payload: schemas.MissionAssign, db: Session = Depends(get_db)):
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    cat = db.query(models.SpyCat).filter(models.SpyCat.id == payload.cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Spy cat not found")

    # check if cat has active mission
    existing = db.query(models.Mission).filter(
        models.Mission.cat_id == payload.cat_id,
        models.Mission.is_complete == False,
        models.Mission.id != mission_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Cat already has an active mission")

    mission.cat_id = payload.cat_id
    db.commit()
    db.refresh(mission)
    return mission

@router.patch("/{mission_id}/targets/{target_id}", response_model=schemas.TargetResponse)
def update_target(
    mission_id: int,
    target_id: int,
    payload: schemas.TargetUpdate,
    db: Session = Depends(get_db),
):
    mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    target = db.query(models.Target).filter(
        models.Target.id == target_id,
        models.Target.mission_id == mission_id,
    ).first()
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    if payload.notes is not None:
        if mission.is_complete or target.is_complete:
            raise HTTPException(status_code=400, detail="Cannot update notes on completed target or mission")
        target.notes = payload.notes

    if payload.is_complete is not None:
        target.is_complete = payload.is_complete

        if target.is_complete:
            all_targets = db.query(models.Target).filter(models.Target.mission_id == mission_id).all()
            if all(t.is_complete for t in all_targets):
                mission.is_complete = True

    db.commit()
    db.refresh(target)
    return target

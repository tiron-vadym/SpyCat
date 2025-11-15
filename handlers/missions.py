from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from sqlalchemy.orm import Session

from models.mission import Mission, Target
from models.cat import Cat
from schemas.missions import MissionCreate, TargetUpdate


def insert_mission(data: MissionCreate, db: Session):
    mission = Mission(cat_id=data.cat_id, complete=data.complete)

    for t in data.targets:
        mission.targets.append(Target(**t.model_dump()))

    db.add(mission)
    db.commit()
    db.refresh(mission)
    return mission


def assign_cat(mission_id: int, cat_id: int, db: Session):
    mission = db.get(Mission, mission_id)
    if mission is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Mission not found")

    cat = db.get(Cat, cat_id)
    if cat is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Cat not found")

    mission.cat_id = cat_id
    db.commit()
    db.refresh(mission)
    return mission


def update_mission_target(mission_id: int, target_id: int, payload: TargetUpdate, db: Session):
    target = db.query(Target).filter(
        Target.id == target_id,
        Target.mission_id == mission_id
    ).first()

    if target is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Target not found")

    # перевірка стану
    if target.complete or target.mission.complete:
        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            "Cannot update notes of a completed target or mission"
        )

    # оновлення
    if payload.notes is not None:
        target.notes = payload.notes

    if payload.complete is not None:
        target.complete = payload.complete

    db.commit()
    db.refresh(target)
    return target


def list_missions(db: Session):
    return db.query(Mission).all()


def retrieve_mission(mission_id: int, db: Session):
    mission = db.get(Mission, mission_id)
    if mission is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Mission not found")
    return mission


def remove_mission(mission_id: int, db: Session):
    mission = db.get(Mission, mission_id)
    if mission is None:
        raise HTTPException(HTTP_404_NOT_FOUND, f"Mission {mission_id} not found")

    if mission.cat_id:
        raise HTTPException(
            HTTP_400_BAD_REQUEST,
            "Cannot delete a mission assigned to a cat"
        )

    db.delete(mission)
    db.commit()

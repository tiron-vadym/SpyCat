from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT

from dependencies import get_db
from handlers.missions import (
    insert_mission,
    assign_cat,
    update_mission_target,
    list_missions,
    remove_mission, retrieve_mission
)
from schemas.missions import MissionOut, MissionCreate, TargetUpdate

router = APIRouter(prefix="/missions", tags=["missions"])


@router.post("/", response_model=MissionOut)
def create_mission(data: MissionCreate, db: Session = Depends(get_db)):
    mission = insert_mission(data, db)
    return mission


@router.post("/{mission_id}/assign/{cat_id}", status_code=HTTP_204_NO_CONTENT)
def assign_task(mission_id: int, cat_id: int, db: Session = Depends(get_db)):
    assign_cat(mission_id, cat_id, db)


@router.patch("/{mission_id}/target/{target_id}", status_code=HTTP_204_NO_CONTENT)
def update_target(
        mission_id: int,
        target_id: int,
        upd: TargetUpdate,
        db: Session = Depends(get_db)
):
    update_mission_target(mission_id, target_id, upd, db)


@router.get("/", response_model=list[MissionOut])
def get_missions(db: Session = Depends(get_db)):
    return list_missions(db)


@router.get("/{mission_id}", response_model=MissionOut)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    return retrieve_mission(mission_id, db)


@router.delete("/{mission_id}", status_code=HTTP_204_NO_CONTENT)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    remove_mission(mission_id, db)

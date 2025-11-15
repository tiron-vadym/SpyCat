from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT

from dependencies import get_db
from handlers.cats import (
    insert_cat,
    retrieve_cat,
    list_cats,
    delete_cat,
    update_salary
)
from schemas.cats import CatOut, CatCreate, CatUpdate

router = APIRouter(prefix="/cats", tags=["cats"])


@router.post("/", response_model=CatOut)
def create_cat(cat: CatCreate, db: Session = Depends(get_db)):
    db_cat = insert_cat(cat, db)
    return db_cat


@router.get("/{cat_id}", response_model=CatOut)
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = retrieve_cat(cat_id, db)
    return cat


@router.get("/", response_model=list[CatOut])
def get_cats(db: Session = Depends(get_db)):
    cats = list_cats(db)
    return cats


@router.patch("/{cat_id}/salary", response_model=CatOut)
def patch_salary(cat_id: int, payload: CatUpdate, db: Session = Depends(get_db)):
    cat = update_salary(cat_id, payload, db)
    return cat


@router.delete("/{cat_id}", status_code=HTTP_204_NO_CONTENT)
def remove_cat(cat_id: int, db: Session = Depends(get_db)):
    delete_cat(cat_id, db)

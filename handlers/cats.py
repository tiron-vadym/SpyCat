from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from sqlalchemy.orm import Session

from models.cat import Cat
from schemas.cats import CatCreate, CatUpdate, CatOut


def insert_cat(cat: CatCreate, db: Session) -> CatOut:
    db_cat = Cat(**cat.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return CatOut.model_validate(db_cat, from_attributes=True)


def list_cats(db: Session):
    cats = db.query(Cat).all()
    return [CatOut.model_validate(cat) for cat in cats]


def retrieve_cat(cat_id: int, db: Session) -> CatOut:
    cat = db.get(Cat, cat_id)
    if cat is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )
    return CatOut.model_validate(cat)


def update_salary(cat_id: int, payload: CatUpdate, db: Session) -> CatOut:
    cat = db.get(Cat, cat_id)
    if cat is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )

    cat.salary = payload.salary
    db.commit()
    db.refresh(cat)
    return CatOut.model_validate(cat)


def delete_cat(cat_id: int, db: Session) -> None:
    cat = db.get(Cat, cat_id)
    if cat is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )
    db.delete(cat)
    db.commit()

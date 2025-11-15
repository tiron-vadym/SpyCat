from pydantic import BaseModel, field_validator, Field
import httpx

from common_models import BaseModelORM
from config import settings


class CatBase(BaseModelORM):
    name: str
    years_of_experience: int
    breed: str
    salary: float


class CatCreate(CatBase):
    @field_validator("breed", mode="before")
    def validate_breed(cls, v: str) -> str:
        try:
            resp = httpx.get(settings.THECATAPI_SEARCH, timeout=5.0)
            resp.raise_for_status()
        except Exception:
            raise ValueError(f"TheCatAPI is unavailable")

        data = resp.json()
        for item in data:
            if item.get("name", "").lower() == v.lower():
                return v

        raise ValueError(f"Breed '{v}' not found in TheCatAPI")


class CatOut(CatBase):
    id: int


class CatUpdate(BaseModel):
    salary: float = Field(ge=0)

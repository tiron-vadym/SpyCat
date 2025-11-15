from pydantic import BaseModel, model_validator

from common_models import BaseModelORM


class TargetCreate(BaseModel):
    name: str
    country: str
    notes: str | None
    complete: bool = False


class TargetUpdate(BaseModel):
    notes: str | None
    complete: bool


class TargetOut(TargetCreate):
    id: int


class MissionCreate(BaseModel):
    cat_id: int | None
    complete: bool = False
    targets: list[TargetCreate]

    @model_validator(mode="before")
    def check_targets_length(cls, values):
        targets = values.get("targets")
        if not targets or not (1 <= len(targets) <= 3):
            raise ValueError("A mission must have between 1 and 3 targets")
        return values


class MissionUpdateTargets(BaseModel):
    targets: list[TargetUpdate]


class MissionOut(BaseModelORM):
    id: int
    cat_id: int | None
    complete: bool
    targets: list[TargetOut]

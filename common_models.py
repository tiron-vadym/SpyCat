from pydantic import BaseModel


class BaseModelORM(BaseModel):
    model_config = {
        "from_attributes": True
    }

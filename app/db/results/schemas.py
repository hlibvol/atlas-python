from typing import Any, Dict, AnyStr, List
from pydantic import BaseModel
from datetime import datetime
from app.db.users.schemas import UserName


class ResultBase(BaseModel):
    objective_id: int = None
    value: float = None
    created_by: int = None
    updated_by: int = None


class ResultEdit(ResultBase):
    class Config:
        orm_mode = True


class ResultOut(ResultBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None
    created_by_user: UserName = None
    updated_by_user: UserName = None

    class Config:
        orm_mode = True

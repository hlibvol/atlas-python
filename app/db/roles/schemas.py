from pydantic import BaseModel
import typing as t


class RoleBase(BaseModel):
    name: str
    description: str = None


class RoleCreate(RoleBase):
    name: str
    description: str = None

    class Config:
        orm_mode = True


class RoleEdit(RoleBase):
    class Config:
        orm_mode = True


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True

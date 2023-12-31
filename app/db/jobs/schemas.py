from app.db.application_types.schemas import ApplicationTypeOut
from pydantic import BaseModel
from app.db.roles.schemas import Role
from app.db.application_urls.schemas import ApplicationUrlOut
from typing import List, Any, Dict, AnyStr, Optional
from enum import Enum
from datetime import datetime
from app.db.users.schemas import UserName


class JobBase(BaseModel):
    name: str = None
    description: str = None
    is_locked: bool = None
    steps: Dict[AnyStr, Any] = None
    is_template: bool = None
    created_by: int = None
    updated_by: int = None


class JobEdit(JobBase):
    application_url_id: int = None
    application_type_id: int = None
    role_ids: Optional[List[int]] = []
    screen_ids: Optional[List[int]] = []
    use_case_ids: Optional[List[int]] = []

    class Config:
        orm_mode = True


class JobOut(JobBase):
    id: int
    application_url: ApplicationUrlOut = None
    roles: List[Role] = None
    role_ids: Optional[List[int]] = []
    screen_ids: Optional[List[int]] = []
    use_case_ids: Optional[List[int]] = []
    application_url_id: int = None
    application_type_id: int = None
    application_type: ApplicationTypeOut = None
    created_at: datetime = None
    updated_at: datetime = None
    created_by_user: UserName = None
    updated_by_user: UserName = None

    class Config:
        orm_mode = True


class ExtensionMode(str, Enum):
    """The possible modes for extension"""

    DESIGNER = "D"
    EXECUTOR = "E"

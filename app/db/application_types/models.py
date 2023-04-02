from sqlalchemy import Column, Integer, String

from app.db.session import Base
from app.db.core import CoreBase, TrackTimeMixin


class ApplicationType(Base, CoreBase, TrackTimeMixin):
    __tablename__ = "application_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
from .database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Integer
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(String, index=True)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

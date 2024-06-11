from datetime import datetime
from typing import List
from pydantic import BaseModel


class TaskBaseSchema(BaseModel):
    id: int | None = None
    title: str
    description: str
    status: str 
    createdAt: datetime | None = None
    

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListTaskResponse(BaseModel):
    status: str
    results: int
    tasks: List[TaskBaseSchema]


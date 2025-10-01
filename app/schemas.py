from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    todo = "à faire"
    in_progress = "en cours"
    done = "terminé"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    due_date: Optional[date] = Field(None, alias="date_limite")

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[date] = Field(None, alias="date_limite")

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True

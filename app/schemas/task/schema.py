from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import EmailStr, Field

from app.schemas.base import BaseSchema


class TaskAssigneeSchema(BaseSchema):
    __slots__ = ()

    user_id: UUID = Field(..., alias="id")
    username: str
    email: EmailStr
    first_name: str
    last_name: str


class TaskProjectSchema(BaseSchema):
    __slots__ = ()

    id: UUID
    title: str


class TaskSchema(BaseSchema):
    __slots__ = ()

    id: UUID
    title: str
    description: str
    task_number: int
    completed: bool
    assignee: Optional[TaskAssigneeSchema] = Field(None, alias="assignee")
    project: Optional[TaskProjectSchema] = Field(None, alias="project")
    created_at: datetime
    updated_at: datetime


class CreateTaskSchema(BaseSchema):
    __slots__ = ()

    title: str
    description: str


class UpdateTaskSchema(BaseSchema):
    __slots__ = ()

    title: str
    description: str
    completed: bool
    assignee_id: Optional[UUID] = None


# RESPONSES

class DeleteTaskResponseSchema(BaseSchema):
    __slots__ = ()

    message: str = "Task deleted"

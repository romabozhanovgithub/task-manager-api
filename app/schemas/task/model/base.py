from typing import Optional
from uuid import UUID

from app.schemas.base import ModelSchema
from app.models import Task


class TaskModel(ModelSchema):
    __slots__ = ()

    title: Optional[str] = None
    description: Optional[str] = None
    task_number: Optional[int] = None
    completed: Optional[bool] = None
    project_id: Optional[UUID] = None
    assignee_id: Optional[UUID] = None

    def to_db(self) -> Task:
        return Task(**self._to_db())

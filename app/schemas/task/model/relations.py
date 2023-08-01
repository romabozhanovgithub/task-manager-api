from typing import Optional
from app.schemas.task.model.base import TaskModel
from app.schemas.user.model.base import UserModel
from app.schemas.project.model.base import ProjectModel


class TaskRelationModel(TaskModel):
    __slots__ = ()

    project: Optional[ProjectModel] = None
    assignee: Optional[UserModel] = None

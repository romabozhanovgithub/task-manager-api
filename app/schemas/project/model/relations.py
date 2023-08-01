from typing import Optional
from app.schemas.project.model.base import ProjectModel
from app.schemas.user.model.base import UserModel
from app.schemas.task.model.base import TaskModel


class ProjectRelationModel(ProjectModel):
    __slots__ = ()

    users: Optional[list[UserModel]] = None
    tasks: Optional[list[TaskModel]] = None

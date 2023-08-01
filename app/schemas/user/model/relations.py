from typing import Optional
from app.schemas.user.model.base import UserModel
from app.schemas.project.model.base import ProjectModel
from app.schemas.task.model.base import TaskModel


class UserRelationModel(UserModel):
    __slots__ = ()

    projects: Optional[list[ProjectModel]] = None
    tasks: Optional[list[TaskModel]] = None

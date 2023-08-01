from typing import Optional

from app.schemas.base import ModelSchema
from app.models import Project


class ProjectModel(ModelSchema):
    __slots__ = ()

    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

    def to_db(self) -> Project:
        return Project(**self._to_db())

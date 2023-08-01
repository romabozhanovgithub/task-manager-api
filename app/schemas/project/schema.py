from typing import Optional
from uuid import UUID

from pydantic import Field, validator
from app.core.exceptions import NotEnoughPermissionsException
from app.models import Role
from app.schemas.base import BaseSchema


def validate_role(role: Role) -> Role:
    if role == Role.OWNER:
        raise NotEnoughPermissionsException
    return role


class ProjectSchema(BaseSchema):
    __slots__ = ()

    id: UUID
    title: str
    description: str
    is_active: bool


class CreateProjectSchema(BaseSchema):
    __slots__ = ()

    title: str
    description: str


class UserProjectSchema(BaseSchema):
    __slots__ = ()

    user_id: UUID
    role: Optional[Role] = None

    @validator("role")
    def validate_role(cls, role: Role) -> Role:
        return validate_role(role)


class UserInProjectSchema(BaseSchema):
    __slots__ = ()

    user_id: UUID = Field(..., alias="id")
    first_name: str
    last_name: str
    role: Role


class UpdateUserProjectSchema(UserProjectSchema):
    __slots__ = ()

    user_id: UUID
    role: Role


class UpdateProjectSchema(BaseSchema):
    __slots__ = ()

    title: str
    description: str
    is_active: bool


# RESPONSES

class AddUserResponseSchema(BaseSchema):
    __slots__ = ()

    message: str = "User added to project"


class UpdateUserResponseSchema(BaseSchema):
    __slots__ = ()

    message: str = "User updated"


class RemoveUserResponseSchema(BaseSchema):
    __slots__ = ()

    message: str = "User removed from project"


class DeleteProjectResponseSchema(BaseSchema):
    __slots__ = ()

    message: str = "Project deleted"

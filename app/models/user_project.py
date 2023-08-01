from enum import Enum
from sqlalchemy import (
    UUID,
    Column,
    Table,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ENUM

from app.models.base import Base


class Role(int, Enum):
    OWNER = 1
    MANAGER = 2
    MEMBER = 3
    GUEST = 4
    

user_project = Table(
    "user_project",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id")),
    Column("project_id", UUID, ForeignKey("projects.id", ondelete="CASCADE")),
    Column("role", ENUM(Role), default=Role.MEMBER),
    UniqueConstraint("user_id", "project_id", name="user_project_uc1"),
)

from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.user_project import user_project


class User(Base):
    __slots__ = ()
    __tablename__ = "users"

    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    projects = relationship(
        "Project", secondary=user_project, back_populates="users"
    )
    tasks = relationship("Task", back_populates="assignee")

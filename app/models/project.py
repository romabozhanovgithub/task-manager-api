from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.user_project import user_project


class Project(Base):
    __slots__ = ()
    __tablename__ = "projects"

    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    users = relationship(
        "User", secondary=user_project, back_populates="projects"
    )
    tasks = relationship("Task", back_populates="project")

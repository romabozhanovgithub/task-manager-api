from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.models.base import Base


class Task(Base):
    __slots__ = ()
    __tablename__ = "tasks"

    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    task_number = Column(Integer, nullable=False, index=True)
    completed = Column(Boolean, default=False)

    project_id = Column(
        UUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    assignee_id = Column(
        UUID, ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ), nullable=True
    )

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")

    __table_args__ = (
        UniqueConstraint(
            "project_id", "task_number", name="unique_task_number_constraint"
        ),
    )

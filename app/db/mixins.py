from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID


class UUIDMixin:
    __slots__ = ()

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )


class TimestampMixin:
    __slots__ = ()

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        onupdate=datetime.utcnow,
    )

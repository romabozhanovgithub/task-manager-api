from sqlalchemy.orm import DeclarativeBase

from app.db.mixins import UUIDMixin, TimestampMixin


class Base(UUIDMixin, TimestampMixin, DeclarativeBase):
    __abstract__ = True

    def __repr__(self):
        columns = ", ".join(
            f"{c.name}={getattr(self, c.name)!r}"
            for c in self.__table__.columns
        )
        return f"<{self.__class__.__name__}({columns})>"

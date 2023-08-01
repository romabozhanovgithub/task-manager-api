from datetime import datetime
from typing import Any, Optional, TypeVar
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from app.models.base import Base


BaseModelConfig = ConfigDict(
    from_attributes=True,
    alias_generator=to_camel,
    populate_by_name=True,
)


class UUIDModelMixin(BaseModel):
    id: Optional[UUID] = None


class TimestampModelMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class BaseModelSchema(BaseModel):
    model_config = BaseModelConfig


class ModelSchema(BaseModelSchema, UUIDModelMixin, TimestampModelMixin):
    def _to_db(self) -> dict[str, Any]:
        data = self.model_dump(
            exclude_none=True,
            exclude_unset=True,
        )
        return data

    def to_db(self) -> TypeVar("Model", bound=Base):
        raise NotImplementedError

from datetime import datetime
from uuid import UUID
from pydantic import EmailStr

from app.schemas.base import BaseSchema


class RequestUser(BaseSchema):
    __slots__ = ()

    id: UUID
    username: str
    email: EmailStr


class ResponseUser(BaseSchema):
    __slots__ = ()

    id: UUID
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

from typing import Optional
from pydantic import EmailStr

from app.schemas.base import ModelSchema
from app.models import User


class UserModel(ModelSchema):
    __slots__ = ()

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

    def to_db(self) -> User:
        return User(**self._to_db())

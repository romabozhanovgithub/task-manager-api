from pydantic import BaseModel, EmailStr

from app.schemas.base import BaseSchema
from app.schemas.user import RequestUser


class TokenDataSchema(RequestUser):
    __slots__ = ()


class TokenSchema(BaseModel):
    __slots__ = ()

    token_type: str = "bearer"


class AccessTokenSchema(TokenSchema):
    __slots__ = ()

    access_token: str


class RefreshTokenSchema(TokenSchema):
    __slots__ = ()

    refresh_token: str


class SignUpUser(BaseSchema):
    __slots__ = ()

    email: EmailStr
    password: str
    first_name: str
    last_name: str


class SignUpResponseSchema(RequestUser):
    __slots__ = ()

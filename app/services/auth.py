from fastapi import Depends
from passlib.context import CryptContext

from app.core.exceptions import (
    InvalidCredentialsException,
    InactiveUserException,
    UserAlreadyExistsException,
)
from app.core.security import jwt_context
from app.repositories import UserRepository
from app.schemas.user import UserModel, RequestUser
from app.schemas.auth import AccessTokenSchema, TokenDataSchema, SignUpUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    __slots__ = ("user_repository",)
    
    def __init__(
        self, user_repository: UserRepository = Depends(UserRepository)
    ) -> None:
        self.user_repository = user_repository

    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    async def authenticate_user(
        self, login: str, password: str
    ) -> AccessTokenSchema:
        auth = login.split("@")
        user = await self.user_repository.get_by_username(auth[0])
        if user and self.verify_password(password, user.password):
            if user.is_active:
                token_data = TokenDataSchema.model_validate(user)
                to_encode = token_data.model_dump_json()
                token = jwt_context.create_access_token(
                    subject=to_encode
                )
                return AccessTokenSchema(access_token=token)
            raise InactiveUserException
        raise InvalidCredentialsException

    async def sign_up_user(self, user: SignUpUser) -> UserModel:
        user_exists = await self.user_repository.get_by_email(user.email)
        if user_exists:
            raise UserAlreadyExistsException

        data: dict[str, str] = user.model_dump()
        data["username"] = data["email"].split("@")[0]
        data["password"] = self.get_password_hash(data["password"])
        user: UserModel = await self.user_repository.create(UserModel(**data))
        return user
    
    async def get_current_user(self, user: RequestUser) -> UserModel:
        user = await self.user_repository.get_by_id(user.id)
        if user is None:
            raise InvalidCredentialsException
        return user

from typing import Sequence
from fastapi import Request
from starlette.authentication import AuthenticationBackend

from app.core.security import jwt_context
from app.schemas.user import RequestUser


class BearerAuthBackend(AuthenticationBackend):
    __slots__ = ()
    
    async def authenticate(
        self, request: Request, *args, **kwargs
    ) -> Sequence[str | RequestUser] | None:
        if "Authorization" not in request.headers:
            return None
        auth = request.headers.get("Authorization")
        try:
            scheme, param = auth.split()
            if scheme.lower() != "bearer":
                return None
            decoded: dict = jwt_context.decode_token(param)
            auth_data = decoded.get("sub")
            user = RequestUser.model_validate_json(auth_data)
            return auth, user
        except Exception as e:
            return None

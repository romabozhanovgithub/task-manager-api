from fastapi import Depends, Request
from starlette.authentication import UnauthenticatedUser

from app.core.exceptions import UnauthorizedException
from app.core.security import JWTContext, jwt_context


class LoginRequiredPermission:
    __slots__ = ()

    def __call__(
        self, request: Request, jwt: JWTContext = Depends(jwt_context)
    ) -> bool:
        if isinstance(request.user, UnauthenticatedUser):
            raise UnauthorizedException
        return True


LoginRequired = LoginRequiredPermission()

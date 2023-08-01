from datetime import datetime, timedelta
from fastapi import Depends, Request

from jose import ExpiredSignatureError, JWTError, jwt
from app.core import settings
from app.core.exceptions import ExpiredTokenException, InvalidTokenException
from app.core.security.utils import oauth_scheme


class JWTContext:
    __slots__ = ()

    def _create_token(self, subject: dict | str, expires: int) -> str:
        """
        Create JWT token.
        """

        expires_delta = datetime.utcnow() + timedelta(minutes=expires)
        to_encode = {"exp": expires_delta, "sub": subject}
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, settings.ALGORITHM
        )
        return encoded_jwt

    def create_access_token(self, subject: dict | str) -> str:
        """
        Create access token.
        """

        return self._create_token(
            subject, settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    def create_refresh_token(self, subject: dict | str) -> str:
        """
        Create refresh token.
        """

        return self._create_token(
            subject, settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

    def decode_token(self, token: str) -> dict[str, str | int]:
        """
        Decode JWT token.
        Throw an error if the token is invalid.
        """

        try:
            decoded_token = jwt.decode(
                token=str(token),
                key=settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
            return decoded_token
        except ExpiredSignatureError:
            raise ExpiredTokenException
        except JWTError:
            raise InvalidTokenException

    def __call__(
        self, token: str = Depends(oauth_scheme)
    ) -> dict[str, str | int] | str | None:
        data = self.decode_token(token)
        return data.get("sub")


jwt_context = JWTContext()

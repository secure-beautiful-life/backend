from typing import Optional, Tuple

from starlette.authentication import AuthenticationBackend, AuthenticationError
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from app.user.repository import UserRepo
from core.exceptions import ExpiredTokenException, UnauthorizedException, InvalidTokenScopeException, \
    DecodeTokenException
from core.fastapi.schemas import CurrentUser
from core.utils.token_helper import TokenHelper


class AuthBackend(AuthenticationBackend):
    def __init__(self):
        self.authentication_white_list = ["/api/users/login"]

    async def authenticate(self, conn: HTTPConnection) -> Tuple[bool, Optional[CurrentUser]]:
        current_user = CurrentUser()

        if conn.url.path in self.authentication_white_list:
            return False, current_user

        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user

        try:
            scheme, token = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, current_user
        except ValueError:
            return False, current_user

        if not token:
            return False, current_user

        try:
            decoded = TokenHelper.decode(token)
            if decoded.get("scope") != "access_token":
                raise AuthenticationError(InvalidTokenScopeException)
            user_id = decoded.get("user_id")
        except DecodeTokenException:
            raise AuthenticationError(DecodeTokenException)
        except ExpiredTokenException:
            raise AuthenticationError(ExpiredTokenException)
        except Exception:
            raise AuthenticationError(UnauthorizedException)

        user = await UserRepo().get_by_id(id=user_id)
        if not user:
            return False, current_user

        current_user.id = user.id
        current_user.role_id = user.role_id
        current_user.token = token
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass

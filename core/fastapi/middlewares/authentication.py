from typing import Optional, Tuple

import jwt
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from app.user.repository import UserRepo
from core.fastapi.schemas import CurrentUser
from core.utils.token_helper import TokenHelper


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> Tuple[bool, Optional[CurrentUser]]:
        current_user = CurrentUser()
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
                return False, current_user
            user_id = decoded.get("user_id")
        except jwt.exceptions.PyJWTError:
            return False, current_user

        user = await UserRepo().get_by_id(id=user_id)
        if not user:
            return False, current_user

        current_user.id = user.id
        current_user.role_id = user.role_id
        current_user.token = token
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
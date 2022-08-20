from datetime import datetime, timedelta
from typing import Union, NoReturn
from zoneinfo import ZoneInfo

import jwt

from core.config import config
from core.exceptions import DecodeTokenException, ExpiredTokenException, InvalidTokenScopeException


class TokenHelper:
    @staticmethod
    def encode(payload: dict, refresh: bool = False) -> str:
        now = datetime.now(tz=ZoneInfo(config.APP_TIMEZONE))
        exp = timedelta(seconds=config.JWT_REFRESH_TOKEN_EXPIRES) if refresh else timedelta(
            seconds=config.JWT_ACCESS_TOKEN_EXPIRES)
        token = jwt.encode(
            payload={
                **payload,
                "exp": now + exp,
                "iat": now,
                "scope": "refresh_token" if refresh else "access_token"
            },
            key=config.JWT_SECRET_KEY,
            algorithm=config.JWT_ALGORITHM,
        )
        return token

    @staticmethod
    def decode(token: str) -> Union[dict, NoReturn]:
        try:
            decoded = jwt.decode(token, config.JWT_SECRET_KEY, config.JWT_ALGORITHM)
            return decoded
        except jwt.exceptions.DecodeError:
            raise DecodeTokenException
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredTokenException

    @staticmethod
    def refresh(token: str) -> Union[str, NoReturn]:
        try:
            decoded = TokenHelper.decode(token)
            if decoded.get("scope") != "refresh_token":
                raise InvalidTokenScopeException
            new_token = TokenHelper.encode(decoded)
            return new_token
        except Exception as e:
            raise e

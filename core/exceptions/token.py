from core.exceptions import UnauthorizedException


class DecodeTokenException(UnauthorizedException):
    message = "토큰 디코딩에 실패했습니다."


class ExpiredTokenException(UnauthorizedException):
    message = "토큰이 만료되었습니다. 다시 로그인해 주세요."


class InvalidTokenScopeException(UnauthorizedException):
    message = "토큰의 scope가 올바르지 않습니다."

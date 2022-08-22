from core.config import config
from core.exceptions import UnauthorizedException


class UserAuthenticationFailedException(UnauthorizedException):
    message = "아이디 혹은 비밀번호가 틀리거나 탈퇴된 사용자입니다."


class UserLoginForbiddenException(UnauthorizedException):
    message = f"로그인에 연속으로 실패하였습니다. {config.LOGIN_FORBIDDEN_TIME}분 뒤에 다시 시도해 주세요."

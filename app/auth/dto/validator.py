from html import escape
from typing import Optional
from urllib.parse import urlparse


def validate_role_name(role_name: str) -> Optional[str]:
    if not (2 <= len(role_name) <= 20):
        raise ValueError("권한 이름은 2자 이상 20자 이하여야 합니다.")

    if not all(character.isalnum() for character in role_name):
        raise ValueError("권한 이름은 한글, 영문 대소문자와 숫자만 포함할 수 있습니다.")

    return escape(role_name)


def validate_role_description(role_description: str) -> Optional[str]:
    if not (2 <= len(role_description) <= 30):
        raise ValueError("권한 설명은 2자 이상 30자 이하여야 합니다.")

    if not all(character.isalnum() for character in role_description):
        raise ValueError("권한 설명은 한글, 영문 대소문자와 숫자만 포함할 수 있습니다.")

    return escape(role_description)


def validate_method(method: str) -> Optional[str]:
    if not all((character.isalpha() and character.isascii()) for character in method):
        raise ValueError("method의 형식이 올바르지 않습니다.")

    if method.upper() not in ["GET", "POST", "PUT", "DELETE"]:
        raise ValueError("지원하지 않는 형식의 method입니다.")

    return method


def validate_url(url: str) -> Optional[str]:
    try:
        urlparse(url).path
    except Exception:
        raise ValueError("url의 형식이 올바르지 않습니다.")

    return url

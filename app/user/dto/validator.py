import re
from html import escape
from typing import Optional


def validate_username(username: str) -> Optional[str]:
    if not (4 <= len(username) <= 10):
        raise ValueError("아이디는 4자 이상 10자 이하여야 합니다.")

    if not all((character.isalnum() and character.isascii()) for character in username):
        raise ValueError("아이디는 영문 대소문자와 숫자만 포함할 수 있습니다.")

    return username


def validate_password(password: str, values: dict, **kwargs) -> Optional[str]:
    if "password" in values and password != values["password"]:
        raise ValueError("비밀번호와 비밀번호 확인값이 일치하지 않습니다.")

    if not (8 <= len(password) <= 20):
        raise ValueError("비밀번호는 8자 이상 20자 이하여야 합니다.")

    if not any(character.islower() for character in password):
        raise ValueError("비밀번호는 영문 소문자를 하나 이상 포함해야 합니다.")

    if not any(character.isupper() for character in password):
        raise ValueError("비밀번호는 영문 대문자를 하나 이상 포함해야 합니다.")

    if not any(character.isdecimal() for character in password):
        raise ValueError("비밀번호는 숫자를 하나 이상 포함해야 합니다.")

    if not any(character in "~!@#$%^&*()-_+=,." for character in password):
        raise ValueError("비밀번호는 특수문자(~!@#$%^&*()-_+=,.)를 하나 이상 포함해야 합니다.")

    return password


def validate_type(type_: str) -> Optional[str]:
    if type_ not in ["brand", "customer"]:
        raise ValueError("회원 종류가 올바르지 않습니다.")

    return type_


def validate_brand_name(brand_name: str) -> Optional[str]:
    if not (2 <= len(brand_name) <= 10):
        raise ValueError("브랜드 이름은 2자 이상 10자 이하여야 합니다.")

    if not all(character.isalnum() for character in brand_name):
        raise ValueError("브랜드 이름은 한글, 영문 대소문자와 숫자만 포함할 수 있습니다.")

    return escape(brand_name)


def validate_gender(gender: str) -> Optional[str]:
    if gender not in ["남성", "여성"]:
        raise ValueError("회원 성별이 올바르지 않습니다.")

    return gender


def validate_email(email: str) -> Optional[str]:
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if not re.fullmatch(regex, email):
        raise ValueError("이메일 형식이 올바르지 않습니다.")

    return email


def validate_phone(phone: str) -> Optional[str]:
    if not len(phone) == 11:
        raise ValueError("전화번호는 '-'를 제외한 11자리 숫자로 입력해 주세요.")

    if not all(character.isdecimal() for character in phone):
        raise ValueError("전화번호는 '-'를 제외한 11자리 숫자로 입력해 주세요.")

    return phone


def validate_address(address: str) -> Optional[str]:
    if not (10 <= len(address) <= 30):
        raise ValueError("주소는 10자 이상 30자 이하여야 합니다.")

    return escape(address)

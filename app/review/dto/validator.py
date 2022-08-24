from html import escape
from typing import Optional


def validate_file_name(file_name: str) -> Optional[str]:
    if not (2 <= len(file_name) <= 50):
        raise ValueError("파일명은 2자 이상 50자 이하여야 합니다.")

    return escape(file_name)


def validate_content(content: str) -> Optional[str]:
    if not (2 <= len(content) <= 100):
        raise ValueError("리뷰는 2자 이상 100자 이하여야 합니다.")

    return escape(content)


def validate_rate(rate: int) -> Optional[int]:
    if not (1 <= rate <= 5):
        raise ValueError("별점은 1점 이상 5점 이하로 입력해 주세요.")

    return rate

from typing import Optional


def validate_amount(amount: int) -> Optional[int]:
    if not (1 <= amount <= 100):
        raise ValueError("수량은 1개 이상 100개 이하로 입력해 주세요.")

    return amount

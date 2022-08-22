from typing import Optional


def validate_name(name: str) -> Optional[str]:
    if not (2 <= len(name) <= 20):
        raise ValueError("상품 이름은 2자 이상 20자 이하여야 합니다.")

    return name


def validate_price(price: int) -> Optional[int]:
    if price < 100:
        raise ValueError("상품 가격은 100원 이상 입력하여야 합니다.")

    return price


def validate_stock_quantity(stock_quantity: int) -> Optional[int]:
    if stock_quantity < 1:
        raise ValueError("상품 수량은 1개 이상 입력하여야 합니다.")

    return stock_quantity

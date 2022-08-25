from html import escape
from typing import Optional


def validate_category_name(name: str) -> Optional[str]:
    if not (2 <= len(name) <= 15):
        raise ValueError("카테고리 이름은 2자 이상 15자 이하여야 합니다.")

    return name


def validate_product_name(name: str) -> Optional[str]:
    if not (2 <= len(name) <= 20):
        raise ValueError("상품 이름은 2자 이상 20자 이하여야 합니다.")

    return name


def validate_file_name(file_name: str) -> Optional[str]:
    if not (2 <= len(file_name) <= 50):
        raise ValueError("파일명은 2자 이상 50자 이하여야 합니다.")

    return escape(file_name)


def validate_price(price: int) -> Optional[int]:
    if price < 100:
        raise ValueError("상품 가격은 100원 이상 입력하여야 합니다.")

    return price


def validate_stock_quantity(stock_quantity: int) -> Optional[int]:
    if stock_quantity < 1:
        raise ValueError("상품 수량은 1개 이상 입력하여야 합니다.")

    return stock_quantity

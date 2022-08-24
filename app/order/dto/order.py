from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, validator

from .validator import validate_amount


class ProductReqeustSchema(BaseModel):
    id: int = Field(..., description="Product ID")
    amount: int = Field(..., description="상품 수량")

    _validate_amount = validator("amount", allow_reuse=True)(validate_amount)


class CreateOrderRequestSchema(BaseModel):
    products: List[ProductReqeustSchema]
    address: str = Field(..., description="배송지")


class ProductResponseSchema(BaseModel):
    id: int = Field(..., description="Product ID")
    profile_image_name: str = Field(..., description="상품 프로필 사진 파일명")
    profile_image_url: str = Field(..., description="상품 프로필 사진 주소")
    name: str = Field(..., description="상품명")
    price: int = Field(..., description="상품 가격(결제 시점 기준)")
    amount: int = Field(..., description="상품 수량")

    class Config:
        orm_mode = True


class GetOrderResponseSchema(BaseModel):
    id: int = Field(..., description="Order ID")
    total_price: int = Field(..., description="총 결제 금액(결제 시점 기준)")
    ordered_products: List[ProductResponseSchema]
    status: str = Field(..., description="주문 상태(ORDERED or CANCELED)")
    address: str = Field(..., description="배송지")
    ordered_date: datetime

    class Config:
        orm_mode = True


class GetOrdertListResponseSchema(BaseModel):
    total_length: int = Field(..., description="전체 리스트 길이")
    content: List[GetOrderResponseSchema]

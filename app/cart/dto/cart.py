from typing import List

from pydantic import BaseModel, Field, validator

from .validator import validate_amount


class CreateCartRequestSchema(BaseModel):
    product_id: int = Field(..., description="아이디(username)")
    amount: int = Field(..., description="비밀번호")

    _validate_amount = validator("amount", allow_reuse=True)(validate_amount)


class GetCartResponseSchema(BaseModel):
    id: int = Field(..., description="Cart ID")
    user_id: int = Field(..., description="User ID")
    product_id: int = Field(..., description="Product ID")
    amount: int = Field(..., description="상품 수량")

    class Config:
        orm_mode = True


class GetCartListResponseSchema(BaseModel):
    total_length: int = Field(..., description="전체 리스트 길이")
    content: List[GetCartResponseSchema]


class UpdateCartRequestSchema(BaseModel):
    amount: int = Field(..., description="비밀번호")

    _validate_amount = validator("amount", allow_reuse=True)(validate_amount)

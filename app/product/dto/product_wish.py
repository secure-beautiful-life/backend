from typing import List

from pydantic import BaseModel, Field

from app.product.dto import SimpleGetProductResponseSchema


class GetWishResponseSchema(BaseModel):
    id: int = Field(..., description="좋아요 아이디")
    user_id: int = Field(..., description="유저 아이디")
    product_id: int = Field(..., description="상품 아이디")
    product: SimpleGetProductResponseSchema = Field(..., description="상품")

    class Config:
        orm_mode = True


class GetWishListResponseSchema(BaseModel):
    content: List[GetWishResponseSchema] = Field(..., description="위시 목록")

    class Config:
        orm_mode = True


class ProductWishRequestSchema(BaseModel):
    product_id: int = Field(..., description="상품 아이디")

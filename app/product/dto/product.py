from typing import List

from pydantic import BaseModel, Field, validator

from .validator import validate_name, validate_price, validate_stock_quantity


class GetProductDetailImageResponseSchema(BaseModel):
    image_name: str = Field(None, description="상품 디테일 사진 파일명")
    image_url: str = Field(None, description="상품 디에틸 사진 주소")


class GetProductResponseSchema(BaseModel):
    category_id: int = Field(..., description="카테고리 아이디")
    product_id: int = Field(..., description="상품 아이디")
    profile_image_name: str = Field(None, description="프로필 사진 파일명")
    profile_image_url: str = Field(None, description="프로필 사진 주소")
    name: str = Field(..., description="상품 이름")
    price: int = Field(..., description="상품 가격")
    brand_name: str = Field(None, description="상품 브랜드 이름")
    detail_images: List[GetProductDetailImageResponseSchema] = Field(..., description="상품 디테일 이미지")
    wish: bool = Field(False, description="상품 좋아요")

    class Config:
        orm_mode = True


class SimpleGetProductResponseSchema(BaseModel):
    category_id: int = Field(..., description="카테고리 아이디")
    product_id: int = Field(..., description="상품 아이디")
    profile_image_name: str = Field(None, description="프로필 사진 파일명")
    profile_image_url: str = Field(None, description="프로필 사진 주소")
    name: str = Field(..., description="상품 이름")
    price: int = Field(..., description="상품 가격")
    brand_name: str = Field(None, description="상품 브랜드 이름")
    wish: bool = Field(False, description="상품 좋아요")

    class Config:
        orm_mode = True


class SimpleGetProductListResponseSchema(BaseModel):
    total_length: int = Field(..., description="길이")
    content: List[SimpleGetProductResponseSchema]


class CreateDetailImageSchema(BaseModel):
    image_string: str = Field(..., description="상품 상세 이미지")
    file_name: str = Field(..., description="상품 상세 이미지 파일 이름")


class CreateProductRequestSchema(BaseModel):
    category_id: int = Field(..., description="카테고리 아이디")
    profile_image_string: str = Field(..., description="상품 프로필 이미지")
    profile_file_name: str = Field(..., description="상품 프로필 이미지 파일 이름")
    name: str = Field(..., description="상품 이름")
    price: int = Field(..., description="상품 가격")
    stock_quantity: int = Field(..., description="재고 수량")
    detail_images: List[CreateDetailImageSchema] = Field(..., description="상품 상세 이미지")

    _validate_name = validator("name", allow_reuse=True)(validate_name)
    _validate_price = validator("price", allow_reuse=True)(validate_price)
    _validate_stock_quantity = validator("stock_quantity", allow_reuse=True)(validate_stock_quantity)


class UpdateProductRequestSchema(BaseModel):
    name: str = Field(..., description="상품 이름")
    price: int = Field(..., description="상품 가격")

    _validate_name = validator("name", allow_reuse=True)(validate_name)
    _validate_price = validator("price", allow_reuse=True)(validate_price)
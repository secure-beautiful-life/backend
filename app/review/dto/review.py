from typing import List

from pydantic import BaseModel, Field, validator

from .validator import validate_content, validate_rate, validate_file_name


class CreateReviewImageRequestSchema(BaseModel):
    image_string: str = Field(..., description="이미지 파일 base64 string")
    file_name: str = Field(..., description="파일명")

    _validate_file_name = validator("file_name", allow_reuse=True)(validate_file_name)


class CreateReviewRequestSchema(BaseModel):
    product_id: int = Field(..., description="아이디(username)")
    content: str = Field(..., description="리뷰 본문")
    rate: int = Field(..., description="별점(1 ~ 5)")
    images: List[CreateReviewImageRequestSchema]

    _validate_content = validator("content", allow_reuse=True)(validate_content)
    _validate_rate = validator("rate", allow_reuse=True)(validate_rate)


class GetReviewImageResponseSchema(BaseModel):
    image_name: str = Field(None, description="리뷰 이미지 파일명")
    image_url: str = Field(None, description="리뷰 이미지 주소")

    class Config:
        orm_mode = True


class GetReviewResponseSchema(BaseModel):
    id: int = Field(..., description="Review ID")
    product_id: int = Field(..., description="Product ID")
    reviewer_name: str = Field(..., description="Product ID")
    content: str = Field(..., description="리뷰 본문")
    rate: int = Field(..., description="별점(1 ~ 5)")
    images: List[GetReviewImageResponseSchema]

    class Config:
        orm_mode = True


class GetReviewListResponseSchema(BaseModel):
    total_length: int = Field(..., description="전체 리스트 길이")
    content: List[GetReviewResponseSchema]

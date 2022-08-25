from pydantic import BaseModel, Field


class GetBeautySchema(BaseModel):
    user_id: int = Field(..., description="유저 아이디")
    product_id: int = Field(..., description="상품 아이디")
    saved_name: str = Field(..., description="뷰티 이미지")

    class Config:
        orm_mode = True


class CreateBeautySchema(BaseModel):
    product_id: int = Field(..., description="상품 아이디")

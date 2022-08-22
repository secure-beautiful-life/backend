from pydantic import BaseModel, Field


class ProductWishRequestSchema(BaseModel):
    product_id: int = Field(..., description="상품 아이디")

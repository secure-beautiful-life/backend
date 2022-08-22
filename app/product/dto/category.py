from typing import Union, ForwardRef

from pydantic import BaseModel, Field

CategoryResponseSchema = ForwardRef('CategoryResponseSchema')


class CreateCategoryRequestSchema(BaseModel):
    name: str = Field(..., description="카테고리 이름")
    parent_id: Union[int, None] = Field(default=None, description="부모 카테고리 아이디")
from typing import Union, ForwardRef

from pydantic import BaseModel, Field, validator

from .validator import validate_category_name

CategoryResponseSchema = ForwardRef('CategoryResponseSchema')


class CreateCategoryRequestSchema(BaseModel):
    name: str = Field(..., description="카테고리 이름")
    parent_id: Union[int, None] = Field(default=None, description="부모 카테고리 아이디")

    _validate_name = validator("name", allow_reuse=True)(validate_category_name)
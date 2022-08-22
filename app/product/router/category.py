from typing import List, Type

from fastapi import APIRouter, Path

from app.product.dto import (
    CreateCategoryRequestSchema
)
from app.product.model import Category
from app.product.service import CategoryService
from core.dtos import DefaultOpenAPIResponseSchema, RequestSuccessResponseSchema

category_router = APIRouter()


@category_router.get(
    "",
    responses=DefaultOpenAPIResponseSchema.model
)
async def get_category_list() -> List[Type[Category]]:
    return {
        "content": await CategoryService().get_category_list_with_children()
    }


@category_router.post(
    "",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def create_category(request: CreateCategoryRequestSchema):
    await CategoryService().create_category(**request.dict())

    return {}


@category_router.delete(
    "/{category_id}",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def delete_category(
        category_id: int = Path(..., description="CategoryId")
):
    await CategoryService().delete_category(category_id=category_id)

    return {}

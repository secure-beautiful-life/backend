from fastapi import APIRouter, Request

from app.product.dto import ProductWishRequestSchema, GetProductResponseSchema, GetWishListResponseSchema
from app.product.repository import product_model_to_detail_entity, wish_models_to_entities
from core.dtos import DefaultOpenAPIResponseSchema
from app.product.service import ProductWishService

product_wish_router = APIRouter()


@product_wish_router.get(
    "",
    responses=DefaultOpenAPIResponseSchema.model,
    response_model=GetWishListResponseSchema
)
async def get_wish_list(
        base_request: Request,
):
    return {
        "content": wish_models_to_entities(await ProductWishService().get_wish_list(base_request.user.id))
    }


@product_wish_router.post(
    "",
    responses=DefaultOpenAPIResponseSchema.model,
    response_model=GetProductResponseSchema
)
async def create_wish(
        base_request: Request,
        request: ProductWishRequestSchema
):
    product = product_model_to_detail_entity(
        await ProductWishService().create_wish(user_id=base_request.user.id, **request.dict()), base_request.user.id)

    if base_request.user:
        result = await ProductWishService().product_wish_repo.exists_wish(base_request.user.id, request.product_id)

        if result:
            product.wish = True
        else:
            product.wish = False

    return product


@product_wish_router.delete(
    "",
    responses=DefaultOpenAPIResponseSchema.model,
    response_model=GetProductResponseSchema,
)
async def delete_wish(
        base_request: Request,
        request: ProductWishRequestSchema
):
    product = product_model_to_detail_entity(
        await ProductWishService().delete_wish(user_id=base_request.user.id, **request.dict()))

    if base_request.user:
        result = await ProductWishService().product_wish_repo.exists_wish(base_request.user.id, request.product_id)

        if result:
            product.wish = True
        else:
            product.wish = False

    return product
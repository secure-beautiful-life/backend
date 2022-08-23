from fastapi import APIRouter, Request, Query, Path

from app.cart.dto import CreateCartRequestSchema, UpdateCartRequestSchema, \
    GetCartListResponseSchema
from app.cart.service import CartService
from core.dtos import RequestSuccessResponseSchema, DefaultOpenAPIResponseSchema
from fastapi import APIRouter, Request, Query, Path

from app.cart.dto import CreateCartRequestSchema, UpdateCartRequestSchema, \
    GetCartListResponseSchema
from app.cart.service import CartService
from core.dtos import RequestSuccessResponseSchema, DefaultOpenAPIResponseSchema

cart_router = APIRouter()


@cart_router.post(
    "/me",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def create_cart_me(base_request: Request, request: CreateCartRequestSchema):
    await CartService().create_cart_with_user_id(user_id=base_request.user.id, **request.dict())
    return {}


@cart_router.get(
    "/me",
    response_model=GetCartListResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def get_cart_list_me(
        base_request: Request,
        limit: int = Query(10, description="Limit"),
        offset: int = Query(None, description="Offset"),
):
    return {
        "total_length": await CartService().get_cart_count_with_user_id(user_id=base_request.user.id),
        "content": await CartService().get_cart_list_with_user_id(user_id=base_request.user.id, limit=limit,
                                                                  offset=offset)
    }


@cart_router.put(
    "/{cart_id}",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def update_cart(
        request: UpdateCartRequestSchema,
        cart_id: int = Path(..., description="CartId")
):
    await CartService().update_cart_by_id(id=cart_id, **request.dict())
    return {}


@cart_router.delete(
    "/me",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def truncate_cart(
        base_request: Request,
):
    await CartService().truncate_cart_by_user_id(user_id=base_request.user.id)
    return {}


@cart_router.delete(
    "/{cart_id}",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def delete_cart(
        cart_id: int = Path(..., description="CartId")
):
    await CartService().delete_cart_by_id(id=cart_id)
    return {}

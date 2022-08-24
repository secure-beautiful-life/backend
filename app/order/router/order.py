from fastapi import APIRouter, Request, Path, Query

from app.order.dto import CreateOrderRequestSchema, GetOrdertListResponseSchema
from app.order.model import order_models_to_entities
from app.order.service.order import OrderService
from core.dtos import RequestSuccessResponseSchema, DefaultOpenAPIResponseSchema

order_router = APIRouter()


@order_router.post(
    "/me",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def create_order_me(base_request: Request, request: CreateOrderRequestSchema):
    await OrderService().create_order_with_user_id(user_id=base_request.user.id, **request.dict())
    return {}


@order_router.get(
    "/me",
    response_model=GetOrdertListResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def get_order_list_me(
        base_request: Request,
        limit: int = Query(10, description="Limit"),
        offset: int = Query(None, description="Offset"),
):
    return {
        "total_length": await OrderService().get_order_count_with_user_id(user_id=base_request.user.id),
        "content": order_models_to_entities(
            await OrderService().get_order_list_with_user_id(user_id=base_request.user.id, limit=limit,
                                                             offset=offset))
    }


@order_router.put(
    "/{order_id}",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def update_cart_me(
        base_request: Request,
        order_id: int = Path(..., description="Order Id"),
):
    await OrderService().cancel_order_by_id(user_id=base_request.user.id, id=order_id)
    return {}

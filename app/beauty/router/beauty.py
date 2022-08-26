from fastapi import APIRouter, Request, Query, Path

from app.beauty.dto import CreateBeautySchema
from app.beauty.service.beauty import BeautyService
from core.dtos import RequestSuccessResponseSchema, DefaultOpenAPIResponseSchema

beauty_router = APIRouter()


@beauty_router.get(
    "",
    responses=DefaultOpenAPIResponseSchema.model,
)
async def get_beauty_list(
        limit: int = Query(10, description="Limit"),
        offset: int = Query(None, description="Offset"),
):
    await {
        "total_length": await BeautyService().count_all(),
        "content": await BeautyService().get_beauty_list_desc(limit=limit, offset=offset)
    }


@beauty_router.get(
    "/{beauty_id}",
    responses=DefaultOpenAPIResponseSchema.model
)
async def get_beauty(
    beauty_id: int = Path(..., description="BeautyId")
):
    return await BeautyService().get_beauty(beauty_id=beauty_id)


@beauty_router.post(
    "",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def create_beauty(
        base_request: Request,
        request: CreateBeautySchema,
):
    await BeautyService().create_beauty(user_id=base_request.user.id, **request.dict())

    return {}


@beauty_router.delete(
    "/{beauty_id}",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def delete_beauty(
        base_request: Request,
        beauty_id: int = Path(..., description="BeautyId")
):
    await BeautyService().delete_beauty(user_id=base_request.user.id, beauty_id=beauty_id)

    return {}

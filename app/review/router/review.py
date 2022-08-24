from fastapi import APIRouter, Request, Query, Path

from app.review.dto import CreateReviewRequestSchema, GetReviewListResponseSchema, GetReviewResponseSchema
from app.review.model import review_models_to_entities, review_model_to_entity
from app.review.service import ReviewService
from core.dtos import RequestSuccessResponseSchema, DefaultOpenAPIResponseSchema

review_router = APIRouter()


@review_router.post(
    "",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def create_review(base_request: Request, request: CreateReviewRequestSchema):
    await ReviewService().create_review(user_id=base_request.user.id, **request.dict())
    return {}


@review_router.get(
    "/{review_id}",
    response_model=GetReviewResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def get_review(
        review_id: int = Path(..., description="Review ID"),
):
    return review_model_to_entity(await ReviewService().get_review_by_id(id=review_id))


@review_router.get(
    "",
    response_model=GetReviewListResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def get_review_list(
        product_id: int = Query(..., description="Product ID"),
        limit: int = Query(10, description="Limit"),
        offset: int = Query(None, description="Offset"),
):
    return {
        "total_length": await ReviewService().get_review_count_with_product_id(product_id=product_id),
        "content": review_models_to_entities(
            await ReviewService().get_review_list_with_product_id(product_id=product_id, limit=limit,
                                                                  offset=offset))
    }


@review_router.delete(
    "/{review_id}",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def delete_review(
        base_request: Request,
        review_id: int = Path(..., description="Review ID"),
):
    await ReviewService().delete_review_by_id(user_id=base_request.user.id, id=review_id)
    return {}

from fastapi import APIRouter, Path, Query, Request

from app.product.dto import CreateProductRequestSchema, UpdateProductRequestSchema, \
    SimpleGetProductListResponseSchema, \
    GetProductResponseSchema, SendEmailRequestSchema
from app.product.repository import product_models_to_entities, product_model_to_detail_entity
from app.product.service import ProductService, ProductWishService
from core.dtos import DefaultOpenAPIResponseSchema, RequestSuccessResponseSchema

product_router = APIRouter()


@product_router.get(
    "",
    response_model=SimpleGetProductListResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def get_product_list(
        base_request: Request,
        limit: int = Query(10, description="Limit"),
        offset: int = Query(None, description="Offset"),
        category_id: int = Query(None, description="CategoryId")
):
    products = product_models_to_entities(
        await ProductService().get_product_list_by_filter(limit, offset, category_id))

    # 최적화 필요(상품 수 만큼 쿼리 나감) : 문제 심각
    for product in products:
        if base_request.user:
            result = await ProductWishService().product_wish_repo.exists_wish(base_request.user.id, product.id)

            if result:
                product.wish = True
            else:
                product.wish = False

    return {
        "total_length": await ProductService().get_product_filter_count(category_id),
        "content": products
    }


@product_router.get(
    "/{product_id}",
    response_model=GetProductResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model
)
async def get_product_detail(
        base_request: Request,
        product_id: int = Path(..., description="ProductId")
):
    product = product_model_to_detail_entity(await ProductService().get_product_by_id(product_id))

    if base_request.user:
        result = await ProductWishService().product_wish_repo.exists_wish(base_request.user.id, product_id)

        if result:
            product.wish = True
        else:
            product.wish = False

    return product


@product_router.get(
    "/search/autocomplete",
    response_model=SimpleGetProductListResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model
)
async def get_product_search_autocomplete(
        limit: int = Query(10, description="Limit"),
        offset: int = Query(None, description="Offset"),
        name: str = Query("", description="상품 이름"),
):
    return {
        "total_length": await ProductService().get_product_list_search_count(name=name),
        "content": product_models_to_entities(
            await ProductService().get_product_list_search_autocomplete(limit=limit, offset=offset, name=name))
    }


@product_router.post(
    "",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model
)
async def create_product(
        base_request: Request,
        request: CreateProductRequestSchema
):
    await ProductService().create_product(base_request.user.id, **request.dict())

    return {}


@product_router.put(
    "/{product_id}",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model
)
async def update_product(
        base_request: Request,
        request: UpdateProductRequestSchema,
        product_id: int = Path(..., description="ProductId")
):
    await ProductService().update_product(user_id=base_request.user.id, product_id=product_id, **request.dict())

    return {}


@product_router.delete(
    "/{product_id}",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model
)
async def delete_product(
        base_request: Request,
        product_id: int = Path(..., description="ProductId")
):
    await ProductService().delete_product(user_id=base_request.user.id, product_id=product_id)

    return {}


@product_router.post(
    "/email",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model
)
def create_product(
        request: SendEmailRequestSchema
):
    ProductService().send_product_image_to_email(**request.dict())
    return {}

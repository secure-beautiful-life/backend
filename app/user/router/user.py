from fastapi import APIRouter, Path, Query, Request

from app.user.dto import (
    CreateUserRequestSchema,
    GetUserResponseSchema,
    GetUserListResponseSchema,
    UpdateUserPasswordRequestSchema,
    UpdateUserInfoRequestSchema,
    UserLoginRequestSchema,
    UserLoginResponseSchema,
    CreateUserProfileImageRequestSchema,
    UserRefreshRequestSchema,
    UserRefreshResponseSchema
)
from app.user.model import user_model_to_entity, user_models_to_entities
from app.user.service import UserService
from core.dtos import (
    RequestSuccessResponseSchema,
    DefaultOpenAPIResponseSchema
)

user_router = APIRouter()


@user_router.post(
    "",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def create_user(request: CreateUserRequestSchema):
    await UserService().create_user(type_=request.type, **request.dict())
    return {}


@user_router.get(
    "/me",
    response_model=GetUserResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def get_user_me(base_request: Request):
    return user_model_to_entity(await UserService().get_user_by_id(id=base_request.user.id))


@user_router.get(
    "/{user_id}",
    response_model=GetUserResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def get_user(
        user_id: int = Path(..., description="UserId"),
):
    return user_model_to_entity(await UserService().get_user_by_id(id=user_id))


@user_router.get(
    "",
    response_model=GetUserListResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def get_user_list(
        limit: int = Query(10, description="Limit"),
        offset: int = Query(None, description="Offset"),
):
    return {
        "total_length": await UserService().get_user_count(),
        "users": user_models_to_entities(await UserService().get_user_list(limit=limit, offset=offset))
    }


@user_router.put(
    "/me",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def update_user_password_me(base_request: Request, request: UpdateUserPasswordRequestSchema):
    await UserService().update_password_by_id(id=base_request.user.id, **request.dict())
    return {}


@user_router.put(
    "/info/me",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def update_user_info_me(base_request: Request, request: UpdateUserInfoRequestSchema):
    await UserService().update_info_by_id(id=base_request.user.id, **request.dict())
    return {}


@user_router.delete(
    "/me",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def delete_user_me(base_request: Request):
    await UserService().delete_user_by_id(id=base_request.user.id)
    return {}


@user_router.delete(
    "/{user_id}",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def delete_user(
        user_id: int = Path(..., description="UserId"),
):
    await UserService().delete_user_by_id(id=user_id)
    return {}


@user_router.post(
    "/profile/me",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def create_user_profile_image_me(base_request: Request, request: CreateUserProfileImageRequestSchema):
    await UserService().create_user_profile_by_user_id(user_id=base_request.user.id, **request.dict())
    return {}


@user_router.delete(
    "/profile/me",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def delete_user_profile_image_me(base_request: Request):
    await UserService().delete_user_profile_by_user_id(user_id=base_request.user.id)
    return {}


@user_router.post(
    "/login",
    response_model=UserLoginResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def login(request: UserLoginRequestSchema):
    return await UserService().login(**request.dict())


@user_router.post(
    "/refresh",
    response_model=UserRefreshResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
def refresh(request: UserRefreshRequestSchema):
    return UserService().refresh(**request.dict())

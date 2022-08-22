from fastapi import APIRouter, Path, Query

from app.auth.dto import (
    GetRolePriorityResponseSchema,
    UpdateRoleHierarchyRequestSchema,
    CreateRoleRequestSchema,
    GetRoleResonseSchema,
    GetRoleListResonseSchema,
    UpdateRoleRequestSchema,
    CreateResourceRequestSchema,
    GetResourceResponseSchema,
    GetResourceListResponseSchema,
    UpdateResourceRequestSchema
)
from app.auth.model import resource_models_to_entities, resource_model_to_entity
from app.auth.service import AuthService
from core.dtos import (
    RequestSuccessResponseSchema,
    DefaultOpenAPIResponseSchema
)

auth_router = APIRouter()


@auth_router.get(
    "/role/priority",
    response_model=GetRolePriorityResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def get_role_priority():
    return {"priority_list": await AuthService().get_role_priority()}


@auth_router.put(
    "/role/priority",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def update_role_hierarchy(request: UpdateRoleHierarchyRequestSchema):
    await AuthService().update_role_hierarchy(**request.dict())
    return {}


@auth_router.post(
    "/role",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def create_role(request: CreateRoleRequestSchema):
    await AuthService().create_role(**request.dict())
    return {}


@auth_router.get(
    "/role/{role_id}",
    response_model=GetRoleResonseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def get_role(role_id: int = Path(..., description="RoleId")):
    return await AuthService().get_role_by_id(id=role_id)


@auth_router.get(
    "/role",
    response_model=GetRoleListResonseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def get_role_list(
        limit: int = Query(10, description="Limit"),
        offset: int = Query(None, description="Offset"),
):
    return {
        "total_length": await AuthService().get_role_count(),
        "content": await AuthService().get_role_list(limit=limit, offset=offset)
    }


@auth_router.put(
    "/role/{role_id}",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def update_role(request: UpdateRoleRequestSchema, role_id: int = Path(..., description="RoleId")):
    await AuthService().update_role_by_id(id=role_id, **request.dict())
    return {}


# @auth_router.delete(
#     "/role/{role_id}",
#     response_model=RequestSuccessResponseSchema,
#     responses=DefaultOpenAPIResponseSchema.model,
# )
# async def delete_role(role_id: int = Path(..., description="RoleId")):
#     await AuthService().delete_role_by_id(id=role_id)
#     return {}


@auth_router.post(
    "/resource",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def create_resource(request: CreateResourceRequestSchema):
    await AuthService().create_resource(**request.dict())
    return {}


@auth_router.get(
    "/resource/{resource_id}",
    response_model=GetResourceResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def get_resource(resource_id: int = Path(..., description="ResourceId")):
    return resource_model_to_entity(await AuthService().get_resource_by_id(id=resource_id))


@auth_router.get(
    "/resource",
    response_model=GetResourceListResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def get_resource_list(
        limit: int = Query(10, description="Limit"),
        offset: int = Query(None, description="Offset"),
):
    return {
        "total_length": await AuthService().get_resource_count(),
        "content": resource_models_to_entities(await AuthService().get_resource_list(limit=limit, offset=offset))
    }


@auth_router.put(
    "/resource/{resource_id}",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def update_resource(request: UpdateResourceRequestSchema, resource_id: int = Path(..., description="ResourceId")):
    await AuthService().update_resource_by_id(id=resource_id, **request.dict())
    return {}


@auth_router.delete(
    "/resource/{resource_id}",
    response_model=RequestSuccessResponseSchema,
    responses=DefaultOpenAPIResponseSchema.model,
)
async def delete_resource(resource_id: int = Path(..., description="ResourceId")):
    await AuthService().delete_resource_by_id(id=resource_id)
    return {}

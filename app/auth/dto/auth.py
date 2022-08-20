from typing import List

from pydantic import BaseModel, Field, validator

from .validator import (
    validate_role_name,
    validate_role_description,
    validate_method,
    validate_url
)


class GetRolePriorityResponseSchema(BaseModel):
    priority_list: list = Field(..., description="권한 우선순위 목록")


class UpdateRoleHierarchyRequestSchema(BaseModel):
    priority_list: list = Field(..., description="권한 우선순위 목록")


class CreateRoleRequestSchema(BaseModel):
    name: str = Field(..., description="권한 이름")
    description: str = Field(None, description="권한 설명")

    _validate_name = validator("name", allow_reuse=True)(validate_role_name)
    _validate_role_description = validator("description", allow_reuse=True)(validate_role_description)


class GetRoleResonseSchema(BaseModel):
    id: int = Field(..., description="권한 id")
    name: str = Field(..., description="권한 이름")
    description: str = Field(None, description="권한 설명")

    class Config:
        orm_mode = True


class GetRoleListResonseSchema(BaseModel):
    total_length: int = Field(..., description="전체 리스트 길이")
    roles: List[GetRoleResonseSchema]


class UpdateRoleRequestSchema(BaseModel):
    name: str = Field(None, description="권한 이름")
    description: str = Field(None, description="권한 설명")

    _validate_name = validator("name", allow_reuse=True)(validate_role_name)
    _validate_role_description = validator("description", allow_reuse=True)(validate_role_description)


class CreateResourceRequestSchema(BaseModel):
    method: str = Field(..., description="자원 HTTP Method")
    url: str = Field(..., description="자원 url")
    role_name: str = Field(..., description="권한 이름")

    _validate_method = validator("method", allow_reuse=True)(validate_method)
    _validate_url = validator("url", allow_reuse=True)(validate_url)
    _validate_name = validator("role_name", allow_reuse=True)(validate_role_name)


class GetResourceResponseSchema(BaseModel):
    id: int = Field(..., description="자원 id")
    method: str = Field(..., description="자원 HTTP Method")
    url: str = Field(..., description="자원 url")
    role_name: str = Field(..., description="권한 이름")

    class Config:
        orm_mode = True


class GetResourceListResponseSchema(BaseModel):
    total_length: int = Field(..., description="전체 리스트 길이")
    resources: List[GetResourceResponseSchema]


class UpdateResourceRequestSchema(BaseModel):
    method: str = Field(None, description="자원 HTTP Method")
    url: str = Field(None, description="자원 url")
    role_name: str = Field(None, description="권한 이름")

    _validate_method = validator("method", allow_reuse=True)(validate_method)
    _validate_url = validator("url", allow_reuse=True)(validate_url)
    _validate_name = validator("role_name", allow_reuse=True)(validate_role_name)

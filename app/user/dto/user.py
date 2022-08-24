from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, validator

from .validator import (
    validate_username,
    validate_password,
    validate_type,
    validate_name,
    validate_brand_name,
    validate_gender,
    validate_email,
    validate_phone,
    validate_address, validate_file_name
)


class CreateUserRequestSchema(BaseModel):
    username: str = Field(..., description="아이디(username)")
    password: str = Field(..., description="비밀번호")
    password_check: str = Field(..., description="비밀번호 확인")
    role_id: int = Field(..., description="역할 id")
    name: str = Field(..., description="회원 이름")
    type: str = Field(..., description="회원 종류")
    brand_name: str = Field(None, description="브랜드 이름")
    gender: str = Field(..., description="성별")
    email: str = Field(..., description="이메일")
    phone: str = Field(..., description="전화번호")
    address: str = Field(..., description="주소")

    _validate_username = validator("username", allow_reuse=True)(validate_username)
    _validate_password = validator("password_check", allow_reuse=True)(validate_password)
    _validate_name = validator("name", allow_reuse=True)(validate_name)
    _validate_type = validator("type", allow_reuse=True)(validate_type)
    _validate_brand_name = validator("brand_name", allow_reuse=True)(validate_brand_name)
    _validate_gender = validator("gender", allow_reuse=True)(validate_gender)
    _validate_email = validator("email", allow_reuse=True)(validate_email)
    _validate_phone = validator("phone", allow_reuse=True)(validate_phone)
    _validate_address = validator("address", allow_reuse=True)(validate_address)


class GetUserResponseSchema(BaseModel):
    id: int = Field(..., description="PK")
    username: str = Field(..., description="아이디(username)")
    profile_image_name: str = Field(None, description="프로필 사진 파일명")
    profile_image_url: str = Field(None, description="프로필 사진 주소")
    role_id: int = Field(..., description="역할 id")
    role_name: str = Field(..., description="역할 이름")
    name: str = Field(..., description="회원 이름")
    type: str = Field(..., description="회원 종류")
    brand_name: str = Field(None, description="브랜드 이름")
    gender: str = Field(..., description="성별")
    email: str = Field(..., description="메일 주소")
    phone: str = Field(..., description="전화번호")
    address: str = Field(..., description="주소")
    created_at: datetime = Field(..., description="계정 생성일")
    updated_at: datetime = Field(..., description="최종 수정일")

    class Config:
        orm_mode = True


class GetUserListResponseSchema(BaseModel):
    total_length: int = Field(..., description="전체 리스트 길이")
    content: List[GetUserResponseSchema]


class UpdateUserPasswordRequestSchema(BaseModel):
    prev_password: str = Field(..., description="현재 비밀번호")
    password: str = Field(..., description="비밀번호")
    password_check: str = Field(..., description="비밀번호 확인")

    _validate_password = validator("password_check", allow_reuse=True)(validate_password)


class UpdateUserInfoRequestSchema(BaseModel):
    email: str = Field(None, description="메일 주소")
    phone: str = Field(None, description="전화번호")
    address: str = Field(None, description="주소")

    _validate_email = validator("email", allow_reuse=True)(validate_email)
    _validate_phone = validator("phone", allow_reuse=True)(validate_phone)
    _validate_address = validator("address", allow_reuse=True)(validate_address)


class CreateUserProfileImageRequestSchema(BaseModel):
    image_string: str = Field(..., description="이미지 파일 base64 string")
    file_name: str = Field(..., description="파일명")

    _validate_file_name = validator("file_name", allow_reuse=True)(validate_file_name)


class UserLoginRequestSchema(BaseModel):
    username: str = Field(..., description="아이디(username)")
    password: str = Field(..., description="비밀번호")


class UserLoginResponseSchema(BaseModel):
    access_token: str = Field(..., description="jwt access_token")
    refresh_token: str = Field(..., description="jwt refresh_token")


class UserRefreshRequestSchema(BaseModel):
    refresh_token: str = Field(..., description="jwt refresh_token")


class UserRefreshResponseSchema(BaseModel):
    access_token: str = Field(..., description="jwt access_token")
